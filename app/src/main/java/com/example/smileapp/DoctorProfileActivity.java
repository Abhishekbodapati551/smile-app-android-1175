package com.example.smileapp;

import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.EditText;
import android.widget.ImageButton;
import android.widget.ProgressBar;
import android.widget.TextView;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;
import com.example.smileapp.database.AppDatabase;
import com.example.smileapp.models.Appointment;
import com.example.smileapp.models.User;
import com.google.android.material.button.MaterialButton;
import java.util.List;

public class DoctorProfileActivity extends AppCompatActivity {

    private AppDatabase db;
    private String userUid;
    private User doctor;

    private TextView profileName, profileSpecialization, doctorIdText;
    private TextView totalApptsText, confirmedApptsText, pendingApptsText;
    private EditText clinicNameEdit, emailEdit, doctorIdEdit;
    private MaterialButton saveButton;
    private ImageButton backButton;
    private ProgressBar saveProgress;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_doctor_profile);

        db = AppDatabase.getInstance(this);
        userUid = getIntent().getStringExtra("USER_ID");

        profileName = findViewById(R.id.profile_name);
        profileSpecialization = findViewById(R.id.profile_specialization);
        doctorIdText = findViewById(R.id.doctor_id_text);
        totalApptsText = findViewById(R.id.total_appointments_text);
        confirmedApptsText = findViewById(R.id.confirmed_appointments_text);
        pendingApptsText = findViewById(R.id.pending_appointments_text);
        clinicNameEdit = findViewById(R.id.clinic_name_edit);
        emailEdit = findViewById(R.id.email_edit);
        doctorIdEdit = findViewById(R.id.doctor_id_edit);
        saveButton = findViewById(R.id.save_profile_button);
        backButton = findViewById(R.id.back_button);
        saveProgress = findViewById(R.id.save_progress);

        loadDoctorData();

        backButton.setOnClickListener(v -> finish());

        saveButton.setOnClickListener(v -> saveProfile());
    }

    private void loadDoctorData() {
        if (userUid == null) return;
        saveProgress.setVisibility(View.VISIBLE);
        
        new Thread(() -> {
            // 1. Load Local
            doctor = db.appDao().getUserById(userUid);
            
            if (doctor == null || doctor.doctorId == null || doctor.doctorId.equals("null")) {
                // 2. Fetch from Supabase if local is empty
                try {
                    SessionManager sm = new SessionManager(this);
                    User fresh = SupabaseAuthHelper.signInBlocking(sm.getSavedEmail(), sm.getSavedPassword());
                    if (fresh != null) {
                        doctor = fresh;
                        db.appDao().insertUser(fresh);
                    }
                } catch (Exception e) {
                    Log.e("DoctorProfile", "Remote fetch failed", e);
                }
            }

            if (doctor != null) {
                runOnUiThread(() -> {
                    saveProgress.setVisibility(View.GONE);
                    profileName.setText("Dr. " + doctor.name);
                    profileSpecialization.setText(doctor.specialization != null ? doctor.specialization : "Specialist");
                    if (doctorIdText != null) {
                        doctorIdText.setText("Current ID: " + (doctor.doctorId != null ? doctor.doctorId : "Not Set"));
                    }
                    if (doctorIdEdit != null) {
                        doctorIdEdit.setText(doctor.doctorId != null ? doctor.doctorId : "");
                    }
                    clinicNameEdit.setText(doctor.clinicName != null ? doctor.clinicName : "");
                    emailEdit.setText(doctor.email);

                    loadAppointmentStats();
                });
            } else {
                runOnUiThread(() -> {
                    saveProgress.setVisibility(View.GONE);
                    Toast.makeText(this, "Failed to load profile data", Toast.LENGTH_SHORT).show();
                });
            }
        }).start();
    }

    private void loadAppointmentStats() {
        if (doctor == null || doctor.doctorId == null || doctor.doctorId.isEmpty() || doctor.doctorId.equals("null")) return;

        new Thread(() -> {
            List<Appointment> apps = db.appDao().getAppointmentsForDoctor(doctor.doctorId);
            int total = apps.size();
            int confirmed = 0;
            int pending = 0;

            for (Appointment a : apps) {
                if ("confirmed".equalsIgnoreCase(a.status)) {
                    confirmed++;
                } else if ("pending".equalsIgnoreCase(a.status) || "upcoming".equalsIgnoreCase(a.status)) {
                    pending++;
                }
            }

            final int fTotal = total;
            final int fConfirmed = confirmed;
            final int fPending = pending;

            runOnUiThread(() -> {
                totalApptsText.setText(String.valueOf(fTotal));
                confirmedApptsText.setText(String.valueOf(fConfirmed));
                pendingApptsText.setText(String.valueOf(fPending));
            });
        }).start();
    }

    private void saveProfile() {
        if (doctor == null) return;

        String newClinicName = clinicNameEdit.getText().toString().trim();
        String newDocId = doctorIdEdit.getText().toString().trim();

        if (newClinicName.isEmpty()) {
            Toast.makeText(this, "Clinic name cannot be empty", Toast.LENGTH_SHORT).show();
            return;
        }

        if (newDocId.length() != 4) {
            Toast.makeText(this, "Doctor ID must be 4 digits", Toast.LENGTH_SHORT).show();
            return;
        }

        saveButton.setVisibility(View.GONE);
        saveProgress.setVisibility(View.VISIBLE);

        new Thread(() -> {
            // 1. Update Supabase
            boolean success = SupabaseAuthHelper.updateDoctorProfileBlocking(doctor.uid, newDocId, newClinicName);
            
            if (success) {
                // 2. Update Local DB
                doctor.clinicName = newClinicName;
                doctor.doctorId = newDocId;
                db.appDao().updateUser(doctor);

                runOnUiThread(() -> {
                    saveButton.setVisibility(View.VISIBLE);
                    saveProgress.setVisibility(View.GONE);
                    Toast.makeText(this, "Profile and ID updated successfully!", Toast.LENGTH_LONG).show();
                    loadDoctorData(); // Refresh UI
                });
            } else {
                runOnUiThread(() -> {
                    saveButton.setVisibility(View.VISIBLE);
                    saveProgress.setVisibility(View.GONE);
                    Toast.makeText(this, "Update failed. Check your connection.", Toast.LENGTH_SHORT).show();
                });
            }
        }).start();
    }
}
