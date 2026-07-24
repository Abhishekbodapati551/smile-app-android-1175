package com.example.smileapp;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;
import android.widget.Toast;
import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;
import com.example.smileapp.database.AppDatabase;
import com.example.smileapp.models.Appointment;
import com.example.smileapp.models.BrushingLog;
import com.example.smileapp.models.User;
import com.google.android.material.button.MaterialButton;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.Locale;

public class DoctorDashboardActivity extends AppCompatActivity {

    private AppDatabase db;
    private String doctorId;
    private TextView doctorNameText, doctorSubtitleText, doctorIdDisplay;
    private TextView totalPatientsText, todaysApptsText, pendingApprovalsText, pendingReviewsText;
    private RecyclerView appointmentsRecycler, patientsRecycler;
    private DashboardListAdapter appointmentsAdapter, patientsAdapter;
    private List<Appointment> dashboardApps = new ArrayList<>();
    private List<User> dashboardPatients = new ArrayList<>();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_doctor_dashboard);

        db = AppDatabase.getInstance(this);
        doctorId = getIntent().getStringExtra("USER_ID");

        doctorNameText = findViewById(R.id.doctor_name);
        doctorSubtitleText = findViewById(R.id.doctor_subtitle);
        doctorIdDisplay = findViewById(R.id.doctor_id_display);
        totalPatientsText = findViewById(R.id.total_patients_text);
        todaysApptsText = findViewById(R.id.todays_appts_text);
        pendingApprovalsText = findViewById(R.id.pending_approvals_text);
        pendingReviewsText = findViewById(R.id.pending_reviews_text);

        appointmentsRecycler = findViewById(R.id.appointments_mini_recycler);
        patientsRecycler = findViewById(R.id.recent_patients_recycler);

        appointmentsRecycler.setLayoutManager(new LinearLayoutManager(this));
        patientsRecycler.setLayoutManager(new LinearLayoutManager(this));

        appointmentsAdapter = new DashboardListAdapter(true);
        patientsAdapter = new DashboardListAdapter(false);

        appointmentsRecycler.setAdapter(appointmentsAdapter);
        patientsRecycler.setAdapter(patientsAdapter);

        setupClickListeners();
        loadDoctorData();
    }

    private void setupClickListeners() {
        findViewById(R.id.logout_btn).setOnClickListener(v -> {
            new SessionManager(this).logoutUser();
            startActivity(new Intent(this, MainActivity.class));
            finish();
        });

        findViewById(R.id.total_patients_card).setOnClickListener(v -> {
            SupabaseManager.execute(() -> {
                User doctorUser = db.appDao().getUserById(doctorId);
                if (doctorUser != null && doctorUser.doctorId != null) {
                    runOnUiThread(() -> {
                        Intent intent = new Intent(this, PatientManagementActivity.class);
                        intent.putExtra("DOCTOR_ID", doctorUser.doctorId);
                        startActivity(intent);
                    });
                } else {
                    runOnUiThread(() -> Toast.makeText(this, "Doctor ID not set.", Toast.LENGTH_SHORT).show());
                }
            });
        });

        findViewById(R.id.btn_view_all_patients).setOnClickListener(v -> {
            SupabaseManager.execute(() -> {
                User doctorUser = db.appDao().getUserById(doctorId);
                if (doctorUser != null && doctorUser.doctorId != null) {
                    runOnUiThread(() -> {
                        Intent intent = new Intent(this, PatientManagementActivity.class);
                        intent.putExtra("DOCTOR_ID", doctorUser.doctorId);
                        startActivity(intent);
                    });
                }
            });
        });

        findViewById(R.id.appointments_card).setOnClickListener(v -> {
            Intent intent = new Intent(this, DoctorAppointmentManagerActivity.class);
            intent.putExtra("USER_ID", doctorId);
            startActivity(intent);
        });

        findViewById(R.id.btn_manage_appointments_feature).setOnClickListener(v -> {
            Intent intent = new Intent(this, DoctorAppointmentManagerActivity.class);
            intent.putExtra("USER_ID", doctorId);
            startActivity(intent);
        });

        findViewById(R.id.pending_approvals_card).setOnClickListener(v -> {
            SupabaseManager.execute(() -> {
                User doctorUser = db.appDao().getUserById(doctorId);
                if (doctorUser != null && doctorUser.doctorId != null) {
                    runOnUiThread(() -> {
                        Intent intent = new Intent(this, PendingApprovalsActivity.class);
                        intent.putExtra("DOCTOR_ID", doctorUser.doctorId);
                        startActivity(intent);
                    });
                } else {
                    runOnUiThread(() -> Toast.makeText(this, "Doctor ID not set. Please go to Profile.", Toast.LENGTH_SHORT).show());
                }
            });
        });

        findViewById(R.id.pending_reviews_card).setOnClickListener(v -> {
            SupabaseManager.execute(() -> {
                User doctorUser = db.appDao().getUserById(doctorId);
                if (doctorUser != null && doctorUser.doctorId != null) {
                    runOnUiThread(() -> {
                        Intent intent = new Intent(this, PendingReviewsActivity.class);
                        intent.putExtra("DOCTOR_ID", doctorUser.doctorId);
                        startActivity(intent);
                    });
                } else {
                    runOnUiThread(() -> Toast.makeText(this, "Doctor ID not set.", Toast.LENGTH_SHORT).show());
                }
            });
        });

        findViewById(R.id.btn_edit_profile).setOnClickListener(v -> {
            Intent intent = new Intent(this, DoctorProfileActivity.class);
            intent.putExtra("USER_ID", doctorId);
            startActivity(intent);
        });
    }

    private void loadDoctorData() {
        SupabaseManager.execute(() -> {
            // 1. Show local data INSTANTLY
            User currentLocal = db.appDao().getUserById(doctorId);
            if (currentLocal != null) {
                runOnUiThread(() -> updateDoctorUI(currentLocal));
            }

            // 2. Refresh from Supabase in background
            try {
                SessionManager sm = new SessionManager(this);
                if (!sm.getSavedEmail().isEmpty() && !sm.getSavedPassword().isEmpty()) {
                    User freshData = SupabaseAuthHelper.signInBlocking(sm.getSavedEmail(), sm.getSavedPassword());
                    if (freshData != null) {
                        db.appDao().insertUser(freshData);
                        runOnUiThread(() -> updateDoctorUI(freshData));
                    }
                }
            } catch (Exception e) {
                Log.e("DoctorDashboard", "Background sync failed", e);
            }
            
            loadStats();
        });
    }

    private void updateDoctorUI(User doctor) {
        doctorNameText.setText("Welcome, Dr. " + doctor.name);
        if (doctorIdDisplay != null) {
            String displayId = (doctor.doctorId != null && !doctor.doctorId.equals("null")) ? doctor.doctorId : "Not Set (Go to Profile)";
            doctorIdDisplay.setText("Your Doctor ID: " + displayId);
        }
        if (doctor.clinicName != null && !doctor.clinicName.isEmpty()) {
            doctorSubtitleText.setText(doctor.clinicName);
        } else {
            doctorSubtitleText.setText("Hospital Name Not Set");
        }
    }

    private void loadStats() {
        if (doctorId == null) return;
        
        SupabaseManager.execute(() -> {
            User doctor = db.appDao().getUserById(doctorId);
            if (doctor == null || doctor.doctorId == null) return;
            
            String seqId = doctor.doctorId;

            // Fetch in separate parallel threads to save time
            new Thread(() -> {
                try {
                    List<User> latestPatients = SupabaseAuthHelper.fetchPatientsBlocking(seqId);
                    for (User p : latestPatients) db.appDao().insertUser(p);
                    refreshUIFromLocal(seqId);
                } catch (Exception e) { Log.e("DoctorDashboard", "Patient sync failed", e); }
            }).start();

            new Thread(() -> {
                try {
                    List<BrushingLog> latestLogs = SupabaseAuthHelper.fetchPendingBrushingLogsBlocking(seqId);
                    for (BrushingLog log : latestLogs) {
                        log.doctorId = seqId;
                        db.appDao().insertBrushingLog(log);
                    }
                    refreshUIFromLocal(seqId);
                } catch (Exception e) { Log.e("DoctorDashboard", "Logs sync failed", e); }
            }).start();

            new Thread(() -> {
                try {
                    List<Appointment> latestApps = SupabaseAuthHelper.fetchAppointmentsBlocking(seqId);
                    for (Appointment a : latestApps) db.appDao().insertAppointment(a);
                    refreshUIFromLocal(seqId);
                } catch (Exception e) { Log.e("DoctorDashboard", "Appts sync failed", e); }
            }).start();

            // Initial load from local
            refreshUIFromLocal(seqId);
        });
    }

    private void refreshUIFromLocal(String seqId) {
        List<User> patients = db.appDao().getPatientsByDoctor(seqId);
        List<Appointment> apps = db.appDao().getAppointmentsForDoctor(seqId);
        List<User> pendingAppr = db.appDao().getPendingChildren();
        List<BrushingLog> pendingRev = db.appDao().getPendingBrushingLogsForDoctor(seqId);

        runOnUiThread(() -> {
            totalPatientsText.setText(String.valueOf(patients.size()));
            todaysApptsText.setText(String.valueOf(apps.size()));
            
            // Unique reviews only
            List<BrushingLog> uniquePending = new ArrayList<>();
            for (BrushingLog log : pendingRev) {
                boolean found = false;
                for (BrushingLog unique : uniquePending) {
                    if (unique.id == log.id) { found = true; break; }
                }
                if (!found) uniquePending.add(log);
            }
            pendingReviewsText.setText(String.valueOf(uniquePending.size()));
            
            int pendingApprCount = 0;
            for (User u : pendingAppr) if (seqId.equals(u.doctorId)) pendingApprCount++;
            pendingApprovalsText.setText(String.valueOf(pendingApprCount));

            dashboardApps.clear();
            dashboardApps.addAll(apps);
            appointmentsAdapter.notifyDataSetChanged();

            dashboardPatients.clear();
            dashboardPatients.addAll(patients);
            patientsAdapter.notifyDataSetChanged();
        });
    }

    private class DashboardListAdapter extends RecyclerView.Adapter<DashboardListAdapter.ViewHolder> {
        private boolean isAppointment;
        public DashboardListAdapter(boolean isAppointment) { this.isAppointment = isAppointment; }
        @NonNull
        @Override
        public ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
            View view = LayoutInflater.from(parent.getContext()).inflate(R.layout.item_dashboard_list, parent, false);
            return new ViewHolder(view);
        }
        @Override
        public void onBindViewHolder(@NonNull ViewHolder holder, int position) {
            if (isAppointment) {
                if (position < dashboardApps.size()) {
                    Appointment app = dashboardApps.get(position);
                    holder.title.setText(app.childName);
                    SimpleDateFormat sdf = new SimpleDateFormat("MMM dd, hh:mm a", Locale.getDefault());
                    holder.subtitle.setText(app.type + " - " + sdf.format(new Date(app.date)));

                    holder.itemView.setOnClickListener(v -> {
                        Intent intent = new Intent(DoctorDashboardActivity.this, PatientProfileActivity.class);
                        intent.putExtra("PATIENT_ID", app.childId);
                        intent.putExtra("APPOINTMENT_ID", app.id);
                        startActivity(intent);
                    });
                }
            } else {
                if (position < dashboardPatients.size()) {
                    User p = dashboardPatients.get(position);
                    holder.title.setText(p.name);
                    holder.subtitle.setText("Points: " + p.points);
                    
                    holder.itemView.setOnClickListener(v -> {
                        Intent intent = new Intent(DoctorDashboardActivity.this, PatientProfileActivity.class);
                        intent.putExtra("PATIENT_ID", p.uid);
                        startActivity(intent);
                    });
                }
            }
        }
        @Override
        public int getItemCount() { return isAppointment ? dashboardApps.size() : dashboardPatients.size(); }
        class ViewHolder extends RecyclerView.ViewHolder {
            TextView title, subtitle;
            public ViewHolder(@NonNull View v) {
                super(v);
                title = v.findViewById(R.id.item_title);
                subtitle = v.findViewById(R.id.item_subtitle);
            }
        }
    }

    @Override
    protected void onResume() {
        super.onResume();
        loadDoctorData();
    }
}
