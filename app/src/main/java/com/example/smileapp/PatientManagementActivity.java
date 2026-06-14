package com.example.smileapp;

import android.content.Intent;
import android.os.Bundle;
import android.text.InputType;
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
import com.example.smileapp.models.User;
import java.util.ArrayList;
import java.util.List;

public class PatientManagementActivity extends AppCompatActivity {

    private AppDatabase db;
    private RecyclerView recyclerView;
    private PatientAdapter adapter;
    private String doctorId;
    private List<User> patientList = new ArrayList<>();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_patient_management);

        db = AppDatabase.getInstance(this);
        doctorId = getIntent().getStringExtra("DOCTOR_ID");

        if (doctorId == null) {
            doctorId = getIntent().getStringExtra("USER_ID");
        }

        recyclerView = findViewById(R.id.patient_recycler_view);
        recyclerView.setLayoutManager(new LinearLayoutManager(this));
        adapter = new PatientAdapter(patientList);
        recyclerView.setAdapter(adapter);

        loadPatients();
    }

    private void loadPatients() {
        SupabaseManager.execute(() -> {
            // 1. Show local data INSTANTLY
            List<User> localPatients = db.appDao().getPatientsByDoctor(doctorId);
            runOnUiThread(() -> {
                patientList.clear();
                patientList.addAll(localPatients);
                adapter.notifyDataSetChanged();
            });

            // 2. Sync from Supabase in background
            try {
                List<User> latestPatients = SupabaseAuthHelper.fetchPatientsBlocking(doctorId);
                if (!latestPatients.isEmpty()) {
                    for (User u : latestPatients) db.appDao().insertUser(u);
                    
                    runOnUiThread(() -> {
                        patientList.clear();
                        patientList.addAll(latestPatients);
                        adapter.notifyDataSetChanged();
                    });
                }
            } catch (Exception e) {
                Log.e("PatientManagement", "Fetch failed", e);
            }
        });
    }

    private void showRemovePointsDialog(User patient) {
        AlertDialog.Builder builder = new AlertDialog.Builder(this);
        builder.setTitle("Remove Points from " + patient.name);
        EditText input = new EditText(this);
        input.setInputType(InputType.TYPE_CLASS_NUMBER);
        builder.setView(input);

        builder.setPositiveButton("Remove", (dialog, which) -> {
            String value = input.getText().toString();
            if (!value.isEmpty()) {
                int toRemove = Integer.parseInt(value);
                int newPts = Math.max(0, patient.points - toRemove);
                SupabaseManager.execute(() -> {
                    if (SupabaseAuthHelper.removePointsBlocking(patient.uid, newPts)) {
                        db.appDao().removePoints(patient.uid, toRemove);
                        runOnUiThread(this::loadPatients);
                    }
                });
            }
        });
        builder.setNegativeButton("Cancel", null).show();
    }

    private class PatientAdapter extends RecyclerView.Adapter<PatientAdapter.ViewHolder> {
        private List<User> users;
        public PatientAdapter(List<User> users) { this.users = users; }
        @NonNull
        @Override
        public ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
            return new ViewHolder(LayoutInflater.from(parent.getContext()).inflate(R.layout.item_patient, parent, false));
        }
        @Override
        public void onBindViewHolder(@NonNull ViewHolder holder, int position) {
            User p = users.get(position);
            holder.nameText.setText(p.name);
            holder.pointsText.setText("Points: " + p.points);
            
            holder.itemView.setOnClickListener(v -> {
                Intent intent = new Intent(PatientManagementActivity.this, PatientProfileActivity.class);
                intent.putExtra("PATIENT_ID", p.uid);
                startActivity(intent);
            });

            holder.removeBtn.setOnClickListener(v -> showRemovePointsDialog(p));
        }
        @Override
        public int getItemCount() { return users.size(); }
        class ViewHolder extends RecyclerView.ViewHolder {
            TextView nameText, pointsText; View removeBtn;
            public ViewHolder(@NonNull View v) {
                super(v);
                nameText = v.findViewById(R.id.patient_name);
                pointsText = v.findViewById(R.id.patient_points);
                removeBtn = v.findViewById(R.id.remove_points_button);
            }
        }
    }
}
