package com.example.smileapp;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;
import androidx.annotation.NonNull;
import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;
import com.example.smileapp.database.AppDatabase;
import com.example.smileapp.models.BrushingLog;
import com.example.smileapp.models.User;
import com.google.android.material.button.MaterialButton;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.Locale;

public class PendingReviewsActivity extends AppCompatActivity {

    private AppDatabase db;
    private RecyclerView recyclerView;
    private ReviewsAdapter adapter;
    private String doctorId;
    private List<BrushingLog> logList = new ArrayList<>();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_pending_reviews);

        db = AppDatabase.getInstance(this);
        doctorId = getIntent().getStringExtra("DOCTOR_ID");

        if (doctorId == null) {
            Toast.makeText(this, "Doctor ID missing", Toast.LENGTH_SHORT).show();
            finish();
            return;
        }

        recyclerView = findViewById(R.id.reviews_recycler_view);
        recyclerView.setLayoutManager(new LinearLayoutManager(this));
        adapter = new ReviewsAdapter(logList);
        recyclerView.setAdapter(adapter);

        loadLogs();
    }

    private void loadLogs() {
        SupabaseManager.execute(() -> {
            try {
                // 1. Initial load from local Room DB for instant display
                List<BrushingLog> localLogs = db.appDao().getPendingBrushingLogsForDoctor(doctorId);
                List<BrushingLog> initialUnique = deDuplicateLogs(localLogs);
                for (BrushingLog log : initialUnique) {
                    if (log.childName == null || log.childName.isEmpty()) {
                        User child = db.appDao().getUserById(log.childId);
                        if (child != null) log.childName = child.name;
                    }
                }
                
                runOnUiThread(() -> {
                    logList.clear();
                    logList.addAll(initialUnique);
                    adapter.notifyDataSetChanged();
                });

                // 2. Fetch fresh logs from Supabase
                List<BrushingLog> latestLogs = SupabaseAuthHelper.fetchPendingBrushingLogsBlocking(doctorId);
                for (BrushingLog log : latestLogs) {
                    log.doctorId = doctorId;
                    if (log.childName == null || log.childName.isEmpty()) {
                        User child = db.appDao().getUserById(log.childId);
                        if (child != null) log.childName = child.name;
                    }
                    db.appDao().insertBrushingLog(log);
                }

                // 3. Re-query local Room DB after network sync to get complete list
                List<BrushingLog> updatedLocalLogs = db.appDao().getPendingBrushingLogsForDoctor(doctorId);
                List<BrushingLog> finalUnique = deDuplicateLogs(updatedLocalLogs);

                runOnUiThread(() -> {
                    logList.clear();
                    logList.addAll(finalUnique);
                    adapter.notifyDataSetChanged();
                    
                    if (logList.isEmpty()) {
                        Toast.makeText(this, "No videos to review.", Toast.LENGTH_SHORT).show();
                    }
                });
            } catch (Exception e) {
                Log.e("PendingReviews", "Failed to load logs", e);
            }
        });
    }

    private List<BrushingLog> deDuplicateLogs(List<BrushingLog> logs) {
        List<BrushingLog> uniqueLogs = new ArrayList<>();
        for (BrushingLog log : logs) {
            boolean duplicate = false;
            for (BrushingLog existing : uniqueLogs) {
                if (existing.id == log.id) { duplicate = true; break; }
            }
            if (!duplicate) uniqueLogs.add(log);
        }
        return uniqueLogs;
    }

    private class ReviewsAdapter extends RecyclerView.Adapter<ReviewsAdapter.ViewHolder> {
        private List<BrushingLog> logs;
        public ReviewsAdapter(List<BrushingLog> logs) { this.logs = logs; }
        
        @NonNull
        @Override
        public ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
            return new ViewHolder(LayoutInflater.from(parent.getContext()).inflate(R.layout.item_pending_review, parent, false));
        }
        
        @Override
        public void onBindViewHolder(@NonNull ViewHolder holder, int position) {
            BrushingLog l = logs.get(position);
            
            if (l.childName != null && !l.childName.isEmpty()) {
                holder.nameText.setText("Child: " + l.childName);
            } else {
                String displayId = l.childId != null && l.childId.length() >= 8 ? l.childId.substring(0, 8) : "Unknown";
                holder.nameText.setText("Child ID: " + displayId);
            }

            holder.timeText.setText(new SimpleDateFormat("MMM dd, hh:mm a", Locale.getDefault()).format(new Date(l.timestamp)));
            
            holder.viewBtn.setOnClickListener(v -> {
                Intent intent = new Intent(PendingReviewsActivity.this, VideoPlayerActivity.class);
                intent.putExtra("VIDEO_URL", l.videoUri);
                startActivity(intent);

                EditText input = new EditText(PendingReviewsActivity.this);
                input.setHint("Feedback...");
                new AlertDialog.Builder(PendingReviewsActivity.this)
                    .setTitle("Review Brushing Video")
                    .setView(input)
                    .setPositiveButton("Approve", (d, w) -> {
                        String feedback = input.getText().toString();
                        
                        // INSTANT UI REMOVAL: Remove from screen immediately
                        int itemPos = logList.indexOf(l);
                        if (itemPos != -1) {
                            logList.remove(itemPos);
                            adapter.notifyItemRemoved(itemPos);
                        }

                        SupabaseManager.execute(() -> {
                            boolean success = SupabaseAuthHelper.approveBrushingBlocking(String.valueOf(l.id), feedback);
                            if (success) {
                                db.appDao().approveBrushingLog(l.id);
                                runOnUiThread(() -> {
                                    Toast.makeText(PendingReviewsActivity.this, "Approved Successfully! 5 Points Awarded 🎉", Toast.LENGTH_SHORT).show();
                                });
                            } else {
                                runOnUiThread(() -> {
                                    Toast.makeText(PendingReviewsActivity.this, "Approval failed. Refreshing list...", Toast.LENGTH_SHORT).show();
                                    loadLogs();
                                });
                            }
                        });
                    })
                    .setNegativeButton("Reject", (d, w) -> {
                        String feedback = input.getText().toString();
                        if (feedback.isEmpty()) {
                            Toast.makeText(PendingReviewsActivity.this, "Please provide feedback for rejection", Toast.LENGTH_SHORT).show();
                            return;
                        }

                        // INSTANT UI REMOVAL
                        int itemPos = logList.indexOf(l);
                        if (itemPos != -1) {
                            logList.remove(itemPos);
                            adapter.notifyItemRemoved(itemPos);
                        }

                        SupabaseManager.execute(() -> {
                            boolean success = SupabaseAuthHelper.rejectBrushingBlocking(String.valueOf(l.id), feedback);
                            if (success) {
                                runOnUiThread(() -> {
                                    Toast.makeText(PendingReviewsActivity.this, "Video Rejected", Toast.LENGTH_SHORT).show();
                                });
                            } else {
                                runOnUiThread(() -> {
                                    Toast.makeText(PendingReviewsActivity.this, "Rejection failed.", Toast.LENGTH_SHORT).show();
                                    loadLogs();
                                });
                            }
                        });
                    })
                    .setNeutralButton("Cancel", null)
                    .show();
            });
        }
        
        @Override
        public int getItemCount() { return logs.size(); }

        class ViewHolder extends RecyclerView.ViewHolder {
            TextView nameText, timeText; MaterialButton viewBtn;
            public ViewHolder(@NonNull View v) {
                super(v);
                nameText = v.findViewById(R.id.child_name);
                timeText = v.findViewById(R.id.timestamp);
                viewBtn = v.findViewById(R.id.view_video_button);
            }
        }
    }
}
