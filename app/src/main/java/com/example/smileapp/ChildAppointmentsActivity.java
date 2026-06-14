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
    private TextView typeText, dateText, timeText, doctorNameText, locationText, contactText;

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

        findViewById(R.id.back_button).setOnClickListener(v -> finish());

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
            long now = System.currentTimeMillis();
            for (Appointment a : appts) {
                if (a.date > now) {
                    if (latest == null || a.date < latest.date) {
                        latest = a;
                    }
                }
            }

            if (latest != null) {
                Appointment finalLatest = latest;
                runOnUiThread(() -> {
                    typeText.setText(finalLatest.type);
                    
                    SimpleDateFormat dateSdf = new SimpleDateFormat("EEE, MMM dd", Locale.getDefault());
                    SimpleDateFormat timeSdf = new SimpleDateFormat("hh:mm a", Locale.getDefault());
                    
                    dateText.setText(dateSdf.format(new Date(finalLatest.date)));
                    timeText.setText(timeSdf.format(new Date(finalLatest.date)));
                    
                    // Fetch Doctor Details
                    SupabaseManager.execute(() -> {
                        // First try searching by the sequential ID (e.g. 1176)
                        User doctor = db.appDao().getUserBySequentialId(finalLatest.doctorId);
                        
                        // If not found in local DB, it might be a new doctor, just show the placeholder
                        if (doctor != null) {
                            runOnUiThread(() -> {
                                doctorNameText.setText("Dr. " + doctor.name);
                                locationText.setText(doctor.clinicName != null ? doctor.clinicName : "Smile Bright Clinic");
                                contactText.setText(doctor.email);
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
                    typeText.setText("No Appointments");
                    dateText.setText("N/A");
                    timeText.setText("N/A");
                    Toast.makeText(this, "No upcoming appointments found.", Toast.LENGTH_SHORT).show();
                    // Don't finish(), let the user see the screen
                });
            }
        });
    }
}
