package com.example.smileapp;

import android.os.Bundle;
import android.view.View;
import android.widget.TextView;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;
import com.example.smileapp.database.AppDatabase;
import com.example.smileapp.models.Appointment;
import com.example.smileapp.models.User;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.List;
import java.util.Locale;

public class ChildAppointmentsActivity extends AppCompatActivity {

    private AppDatabase db;
    private String userId;
    private TextView typeText, dateText, timeText, doctorNameText, locationText, contactText, statusText;
    private View detailsContainer, emptyContainer;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_child_appointments);

        db = AppDatabase.getInstance(this);
        userId = getIntent().getStringExtra("USER_ID");

        typeText = findViewById(R.id.appt_type_val);
        dateText = findViewById(R.id.val_date);
        timeText = findViewById(R.id.val_time);
        doctorNameText = findViewById(R.id.val_doctor);
        locationText = findViewById(R.id.val_location);
        contactText = findViewById(R.id.val_contact);
        statusText = findViewById(R.id.appt_status_text);

        detailsContainer = findViewById(R.id.appointment_details_container);
        emptyContainer = findViewById(R.id.empty_schedule_container);

        findViewById(R.id.back_button).setOnClickListener(v -> finish());
        
        View refreshBtn = findViewById(R.id.refresh_btn);
        if (refreshBtn != null) {
            refreshBtn.setOnClickListener(v -> {
                Toast.makeText(this, "Refreshing schedule...", Toast.LENGTH_SHORT).show();
                loadAppointment();
            });
        }

        loadAppointment();
    }

    private void loadAppointment() {
        if (userId == null) return;

        SupabaseManager.execute(() -> {
            // 1. Fetch fresh appointments from Supabase first
            try {
                List<Appointment> freshAppts = SupabaseAuthHelper.fetchAppointmentsForChildBlocking(userId);
                for (Appointment a : freshAppts) {
                    db.appDao().insertAppointment(a);
                }
            } catch (Exception e) {
                // Ignore sync errors, fallback to local
            }

            // 2. Get most recent upcoming appointment from local DB (now synced)
            List<Appointment> appts = db.appDao().getAppointmentsForChild(userId);
            Appointment latest = null;
            for (Appointment a : appts) {
                if ("upcoming".equals(a.status) || "confirmed".equals(a.status)) {
                    if (latest == null || a.date < latest.date) {
                        latest = a;
                    }
                }
            }

            if (latest != null) {
                Appointment finalLatest = latest;
                runOnUiThread(() -> {
                    if (detailsContainer != null) detailsContainer.setVisibility(View.VISIBLE);
                    if (emptyContainer != null) emptyContainer.setVisibility(View.GONE);

                    typeText.setText(finalLatest.type != null && !finalLatest.type.isEmpty() ? finalLatest.type : "Dental Checkup");

                    SimpleDateFormat dateSdf = new SimpleDateFormat("EEE, MMM dd, yyyy", Locale.getDefault());
                    SimpleDateFormat timeSdf = new SimpleDateFormat("hh:mm a", Locale.getDefault());

                    dateText.setText(dateSdf.format(new Date(finalLatest.date)));
                    timeText.setText(timeSdf.format(new Date(finalLatest.date)));

                    if (statusText != null) {
                        String st = finalLatest.status != null ? finalLatest.status.toUpperCase() : "UPCOMING";
                        statusText.setText(st);
                    }

                    // Fetch Doctor Details
                    SupabaseManager.execute(() -> {
                        User doctor = db.appDao().getUserBySequentialId(finalLatest.doctorId);

                        if (doctor != null) {
                            runOnUiThread(() -> {
                                doctorNameText.setText("Dr. " + doctor.name);
                                locationText.setText(doctor.clinicName != null && !doctor.clinicName.isEmpty() ? doctor.clinicName : "Smile Bright Clinic");
                                contactText.setText(doctor.email != null ? doctor.email : "Contact via Clinic");
                            });
                        } else {
                            runOnUiThread(() -> {
                                doctorNameText.setText("Dr. Balu");
                                locationText.setText("Smile Bright Clinic");
                                contactText.setText("Contact via Clinic");
                            });
                        }
                    });
                });
            } else {
                runOnUiThread(() -> {
                    if (detailsContainer != null) detailsContainer.setVisibility(View.GONE);
                    if (emptyContainer != null) emptyContainer.setVisibility(View.VISIBLE);
                });
            }
        });
    }
}
