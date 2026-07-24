package com.example.smileapp;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageButton;
import android.widget.TextView;
import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;
import com.example.smileapp.database.AppDatabase;
import com.example.smileapp.models.BrushingLog;
import com.example.smileapp.models.User;
import android.widget.Toast;
import com.example.smileapp.models.Appointment;
import com.google.android.material.button.MaterialButton;
import com.google.android.material.card.MaterialCardView;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.Locale;

public class PatientProfileActivity extends AppCompatActivity {

    private AppDatabase db;
    private String patientUid;
    private int specificApptId = -1;
    private Appointment activeAppt;
    private TextView nameText, emailText, pointsText, streakText;
    private TextView attendanceTitle, activeApptType, activeApptDate;
    private MaterialCardView attendanceCard;
    private MaterialButton btnPresent, btnAbsent;
    private RecyclerView historyRecycler;
    private HistoryAdapter adapter;
    private List<BrushingLog> historyList = new ArrayList<>();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_patient_profile);

        db = AppDatabase.getInstance(this);
        patientUid = getIntent().getStringExtra("PATIENT_ID");
        specificApptId = getIntent().getIntExtra("APPOINTMENT_ID", -1);

        nameText = findViewById(R.id.patient_name);
        emailText = findViewById(R.id.patient_email);
        pointsText = findViewById(R.id.patient_points);
        streakText = findViewById(R.id.patient_streak);

        attendanceTitle = findViewById(R.id.attendance_title);
        attendanceCard = findViewById(R.id.attendance_card);
        activeApptType = findViewById(R.id.active_appt_type);
        activeApptDate = findViewById(R.id.active_appt_date);
        btnPresent = findViewById(R.id.btn_mark_present);
        btnAbsent = findViewById(R.id.btn_mark_absent);

        historyRecycler = findViewById(R.id.brushing_history_recycler);
        ImageButton backBtn = findViewById(R.id.back_button);

        backBtn.setOnClickListener(v -> finish());

        historyRecycler.setLayoutManager(new LinearLayoutManager(this));
        adapter = new HistoryAdapter(historyList);
        historyRecycler.setAdapter(adapter);

        btnPresent.setOnClickListener(v -> markAttendance("present"));
        btnAbsent.setOnClickListener(v -> markAttendance("absent"));

        loadPatientData();
    }

    private void markAttendance(String status) {
        if (activeAppt == null) return;
        activeAppt.status = status;
        
        new Thread(() -> {
            boolean success = SupabaseAuthHelper.updateAppointmentBlocking(activeAppt);
            if (success) {
                db.appDao().updateAppointment(activeAppt);
                
                if ("absent".equals(status)) {
                    String warning = "Note: You were missed at your appointment on " + 
                            new SimpleDateFormat("MMM dd", Locale.getDefault()).format(new Date(activeAppt.date)) + 
                            ". Please contact the clinic.";
                    SupabaseAuthHelper.updateWarningNoteBlocking(patientUid, warning);
                } else {
                    // Clear warning if present
                    SupabaseAuthHelper.updateWarningNoteBlocking(patientUid, null);
                }

                runOnUiThread(() -> {
                    Toast.makeText(this, "Marked as " + status, Toast.LENGTH_SHORT).show();
                    attendanceTitle.setVisibility(View.GONE);
                    attendanceCard.setVisibility(View.GONE);
                    loadPatientData(); // Refresh history
                });
            }
        }).start();
    }

    private void loadPatientData() {
        if (patientUid == null) return;
        SupabaseManager.execute(() -> {
            User patient = db.appDao().getUserById(patientUid);
            List<BrushingLog> logs = db.appDao().getBrushingLogsForChild(patientUid);
            
            // Fetch appointment if needed
            if (specificApptId != -1) {
                activeAppt = null; // Reset
                List<Appointment> allAppts = db.appDao().getAppointmentsForChild(patientUid);
                for (Appointment a : allAppts) if (a.id == specificApptId) { activeAppt = a; break; }
            }

            runOnUiThread(() -> {
                if (patient != null) {
                    nameText.setText(patient.name);
                    emailText.setText(patient.email);
                    pointsText.setText("⭐ " + patient.points);
                    streakText.setText("🔥 " + patient.streak);
                }
                
                if (activeAppt != null && "upcoming".equals(activeAppt.status)) {
                    attendanceTitle.setVisibility(View.VISIBLE);
                    attendanceCard.setVisibility(View.VISIBLE);
                    activeApptType.setText(activeAppt.type);
                    activeApptDate.setText(new SimpleDateFormat("MMM dd, hh:mm a", Locale.getDefault()).format(new Date(activeAppt.date)));
                } else {
                    attendanceTitle.setVisibility(View.GONE);
                    attendanceCard.setVisibility(View.GONE);
                }

                historyList.clear();
                historyList.addAll(logs);
                adapter.notifyDataSetChanged();
            });
        });
    }

    private static class HistoryAdapter extends RecyclerView.Adapter<HistoryAdapter.ViewHolder> {
        private final List<BrushingLog> logs;
        public HistoryAdapter(List<BrushingLog> logs) { this.logs = logs; }

        @NonNull
        @Override
        public ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
            View v = LayoutInflater.from(parent.getContext()).inflate(R.layout.item_dashboard_list, parent, false);
            return new ViewHolder(v);
        }

        @Override
        public void onBindViewHolder(@NonNull ViewHolder holder, int position) {
            BrushingLog log = logs.get(position);
            SimpleDateFormat sdf = new SimpleDateFormat("MMM dd, hh:mm a", Locale.getDefault());
            holder.title.setText(sdf.format(new Date(log.timestamp)));
            holder.subtitle.setText(log.approved ? "Status: Approved" : "Status: Pending");
            holder.subtitle.setTextColor(log.approved ? 0xFF4CAF50 : 0xFFFF9800);
        }

        @Override
        public int getItemCount() { return logs.size(); }

        static class ViewHolder extends RecyclerView.ViewHolder {
            TextView title, subtitle;
            public ViewHolder(@NonNull View v) {
                super(v);
                title = v.findViewById(R.id.item_title);
                subtitle = v.findViewById(R.id.item_subtitle);
            }
        }
    }
}
