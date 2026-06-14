package com.example.smileapp;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.ImageButton;
import android.widget.ProgressBar;
import android.widget.TextView;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;
import com.example.smileapp.database.AppDatabase;
import com.example.smileapp.models.Appointment;
import com.example.smileapp.models.BrushingLog;
import com.example.smileapp.models.User;
import com.google.android.material.card.MaterialCardView;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Date;
import java.util.List;
import java.util.Locale;

public class ChildDashboardActivity extends AppCompatActivity {

    private AppDatabase db;
    private String userId;
    private TextView welcomeText, streakText, taskStatusText;
    private MaterialCardView apptNotificationCard, feedbackCard, rejectionCard;
    private TextView apptDetailsText, feedbackText, rejectionReasonText;
    private ProgressBar taskProgressBar;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_child_dashboard);

        db = AppDatabase.getInstance(this);
        userId = getIntent().getStringExtra("USER_ID");
        
        welcomeText = findViewById(R.id.welcome_user);
        streakText = findViewById(R.id.streak_val);
        taskProgressBar = findViewById(R.id.task_progress);
        taskStatusText = findViewById(R.id.task_status);
        
        apptNotificationCard = findViewById(R.id.appointment_notification_card);
        apptDetailsText = findViewById(R.id.appt_notification_details);
        ImageButton closeNotificationBtn = findViewById(R.id.close_notification_btn);

        feedbackCard = findViewById(R.id.doctor_feedback_card);
        feedbackText = findViewById(R.id.doctor_feedback_text);
        ImageButton closeFeedbackBtn = findViewById(R.id.close_feedback_btn);

        rejectionCard = findViewById(R.id.rejection_card);
        rejectionReasonText = findViewById(R.id.rejection_reason_text);
        ImageButton closeRejectionBtn = findViewById(R.id.close_rejection_btn);

        if (closeNotificationBtn != null) closeNotificationBtn.setOnClickListener(v -> apptNotificationCard.setVisibility(View.GONE));
        if (closeFeedbackBtn != null) closeFeedbackBtn.setOnClickListener(v -> feedbackCard.setVisibility(View.GONE));
        if (closeRejectionBtn != null) closeRejectionBtn.setOnClickListener(v -> rejectionCard.setVisibility(View.GONE));

        setupClickListeners();
        loadUserData();
        startSupabaseListeners();
    }

    private void setupClickListeners() {
        if (apptNotificationCard != null) {
            apptNotificationCard.setOnClickListener(v -> {
                Intent intent = new Intent(this, ChildAppointmentsActivity.class);
                intent.putExtra("USER_ID", userId);
                startActivity(intent);
            });
        }

        findViewById(R.id.btn_appointments_new).setOnClickListener(v -> {
            Intent intent = new Intent(this, ChildAppointmentsActivity.class);
            intent.putExtra("USER_ID", userId);
            startActivity(intent);
        });

        findViewById(R.id.btn_brush_timer).setOnClickListener(v -> {
            Intent intent = new Intent(this, BrushingTipsActivity.class);
            intent.putExtra("USER_ID", userId);
            startActivity(intent);
        });

        findViewById(R.id.btn_rewards).setOnClickListener(v -> {
            Intent intent = new Intent(this, ChildRewardsActivity.class);
            intent.putExtra("USER_ID", userId);
            startActivity(intent);
        });

        findViewById(R.id.logout_btn).setOnClickListener(v -> {
            new SessionManager(this).logoutUser();
            startActivity(new Intent(this, MainActivity.class));
            finish();
        });
    }

    private void startSupabaseListeners() {
        if (userId == null) return;
        SupabaseAuthHelper.listenForAppointments(userId, appt -> {
            // Notification for UPCOMING appointments
            if (appt.date > System.currentTimeMillis()) {
                SimpleDateFormat sdf = new SimpleDateFormat("MMM dd 'at' hh:mm a", Locale.getDefault());
                String formattedDate = sdf.format(new Date(appt.date));
                runOnUiThread(() -> {
                    apptDetailsText.setText(appt.type + ": " + formattedDate);
                    apptNotificationCard.setVisibility(View.VISIBLE);
                });
                SupabaseManager.execute(() -> db.appDao().insertAppointment(appt));
            }
            return kotlin.Unit.INSTANCE;
        });
    }

    private void loadUserData() {
        if (userId == null) return;
        SupabaseManager.execute(() -> {
            // 1. Show local data instantly
            User localUser = db.appDao().getUserById(userId);
            if (localUser != null) {
                runOnUiThread(() -> updateChildUI(localUser));
            }

            // 2. Refresh from Supabase in background
            try {
                SessionManager sm = new SessionManager(this);
                if (!sm.getSavedEmail().isEmpty() && !sm.getSavedPassword().isEmpty()) {
                    User freshUser = SupabaseAuthHelper.signInBlocking(sm.getSavedEmail(), sm.getSavedPassword());
                    if (freshUser != null) {
                        db.appDao().insertUser(freshUser);
                        runOnUiThread(() -> updateChildUI(freshUser));
                    }
                }
            } catch (Exception e) {
                Log.e("ChildDashboard", "Sync failed", e);
            }

            // 3. Sync Brushing Logs to update Progress Bar accurately
            try {
                List<BrushingLog> latestLogs = SupabaseAuthHelper.fetchBrushingLogsForChildBlocking(userId);
                for (BrushingLog log : latestLogs) {
                    db.appDao().insertBrushingLog(log);
                }
            } catch (Exception e) {
                Log.e("ChildDashboard", "Log sync failed", e);
            }

            // 4. Sync Appointments from Supabase
            try {
                List<Appointment> freshAppts = SupabaseAuthHelper.fetchAppointmentsForChildBlocking(userId);
                for (Appointment a : freshAppts) {
                    db.appDao().insertAppointment(a);
                }
            } catch (Exception e) {
                Log.e("ChildDashboard", "Appt sync failed", e);
            }

            // 5. Check for RECENT appointments to show on dashboard
            try {
                // Fetch all appts for this child from cloud
                // We'll use a new method for this or just the dao
                List<Appointment> localAppts = db.appDao().getAppointmentsForChild(userId);
                for (Appointment a : localAppts) {
                    if (a.date > System.currentTimeMillis()) {
                        SimpleDateFormat sdf = new SimpleDateFormat("MMM dd 'at' hh:mm a", Locale.getDefault());
                        String formattedDate = sdf.format(new Date(a.date));
                        runOnUiThread(() -> {
                            apptDetailsText.setText(a.type + ": " + formattedDate);
                            apptNotificationCard.setVisibility(View.VISIBLE);
                        });
                        break; // Just show one
                    }
                }
            } catch (Exception e) {}

            // 5. Check for rejections
            try {
                List<BrushingLog> rejectedLogs = SupabaseAuthHelper.fetchRejectedBrushingLogsBlocking(userId);
                if (!rejectedLogs.isEmpty()) {
                    BrushingLog latest = rejectedLogs.get(0);
                    runOnUiThread(() -> {
                        rejectionReasonText.setText("Please try again. Reason: " + (latest.doctorFeedback != null ? latest.doctorFeedback : "Not clear."));
                        rejectionCard.setVisibility(View.VISIBLE);
                    });
                }
            } catch (Exception e) {
                Log.e("ChildDashboard", "Rejection fetch failed", e);
            }
            
            refreshDailyProgress();
        });
    }

    private void updateChildUI(User user) {
        welcomeText.setText("Hi, " + user.name + "!");
        if (streakText != null) streakText.setText(user.streak + " Days");
    }

    private void refreshDailyProgress() {
        Calendar cal = Calendar.getInstance();
        cal.set(Calendar.HOUR_OF_DAY, 0);
        cal.set(Calendar.MINUTE, 0);
        cal.set(Calendar.SECOND, 0);
        long startOfDay = cal.getTimeInMillis();
        
        cal.set(Calendar.HOUR_OF_DAY, 23);
        cal.set(Calendar.MINUTE, 59);
        cal.set(Calendar.SECOND, 59);
        long endOfDay = cal.getTimeInMillis();

        List<BrushingLog> logsToday = db.appDao().getApprovedBrushingLogsForChildToday(userId, startOfDay, endOfDay);
        int sessionsDone = logsToday.size();

        runOnUiThread(() -> {
            if (taskProgressBar != null) {
                taskProgressBar.setMax(2);
                taskProgressBar.setProgress(sessionsDone);
            }
            if (taskStatusText != null) {
                if (sessionsDone == 0) taskStatusText.setText("0/2 sessions completed");
                else if (sessionsDone == 1) taskStatusText.setText("1/2 sessions completed (50%)");
                else taskStatusText.setText("All tasks done! (100%)");
            }
        });
    }

    @Override
    protected void onResume() {
        super.onResume();
        loadUserData();
    }
}
