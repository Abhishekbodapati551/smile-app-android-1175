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
    private MaterialCardView apptNotificationCard, feedbackCard, rejectionCard, taskCard, warningCard;
    private TextView apptDetailsText, feedbackText, rejectionReasonText, warningText;
    private ProgressBar taskProgressBar;
    private MaterialCardView r1Card, r2Card, r3Card, r4Card;
    private View r1Check, r2Check, r3Check, r4Check;

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

        warningCard = findViewById(R.id.warning_card);
        warningText = findViewById(R.id.warning_text);
        ImageButton closeWarningBtn = findViewById(R.id.close_warning_btn);

        taskCard = findViewById(R.id.task_card);

        r1Card = findViewById(R.id.reward_1_card);
        r2Card = findViewById(R.id.reward_2_card);
        r3Card = findViewById(R.id.reward_3_card);
        r4Card = findViewById(R.id.reward_4_card);
        
        r1Check = findViewById(R.id.reward_1_check);
        r2Check = findViewById(R.id.reward_2_check);
        r3Check = findViewById(R.id.reward_3_check);
        r4Check = findViewById(R.id.reward_4_check);

        if (closeNotificationBtn != null) closeNotificationBtn.setOnClickListener(v -> apptNotificationCard.setVisibility(View.GONE));
        if (closeFeedbackBtn != null) closeFeedbackBtn.setOnClickListener(v -> feedbackCard.setVisibility(View.GONE));
        if (closeRejectionBtn != null) closeRejectionBtn.setOnClickListener(v -> rejectionCard.setVisibility(View.GONE));
        if (closeWarningBtn != null) closeWarningBtn.setOnClickListener(v -> warningCard.setVisibility(View.GONE));

        // Make Feedback and Rejection cards interactive
        if (feedbackCard != null) feedbackCard.setOnClickListener(v -> {
            androidx.appcompat.app.AlertDialog.Builder b = new androidx.appcompat.app.AlertDialog.Builder(this);
            b.setTitle("Doctor's Message").setMessage(feedbackText.getText()).setPositiveButton("OK", null).show();
        });

        if (rejectionCard != null) rejectionCard.setOnClickListener(v -> {
            startActivity(new Intent(this, BrushingTipsActivity.class));
        });

        if (taskCard != null) taskCard.setOnClickListener(v -> {
            Intent intent = new Intent(this, BrushingTipsActivity.class);
            intent.putExtra("USER_ID", userId);
            startActivity(intent);
        });

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
                db.appDao().clearBrushingLogsForChild(userId);
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
                
                // Show the most recent upcoming one on the dashboard
                Appointment latest = null;
                for (Appointment a : freshAppts) {
                    if ("upcoming".equals(a.status)) {
                        if (latest == null || a.date < latest.date) latest = a;
                    }
                }
                
                if (latest != null) {
                    Appointment finalLatest = latest;
                    SimpleDateFormat sdf = new SimpleDateFormat("MMM dd 'at' hh:mm a", Locale.getDefault());
                    String formattedDate = sdf.format(new Date(finalLatest.date));
                    runOnUiThread(() -> {
                        apptDetailsText.setText(finalLatest.type + ": " + formattedDate);
                        apptNotificationCard.setVisibility(View.VISIBLE);
                    });
                } else {
                    runOnUiThread(() -> apptNotificationCard.setVisibility(View.GONE));
                }
            } catch (Exception e) {
                Log.e("ChildDashboard", "Appt sync failed", e);
            }

            // 5. Check for rejections or feedback
            try {
                List<BrushingLog> logs = SupabaseAuthHelper.fetchBrushingLogsForChildBlocking(userId);
                BrushingLog latestRejected = null;
                BrushingLog latestFeedback = null;
                
                for (BrushingLog log : logs) {
                    if (log.isRejected) {
                        if (latestRejected == null || log.timestamp > latestRejected.timestamp) latestRejected = log;
                    }
                    if (log.doctorFeedback != null && !log.doctorFeedback.isEmpty() && !log.isRejected) {
                        if (latestFeedback == null || log.timestamp > latestFeedback.timestamp) latestFeedback = log;
                    }
                }
                
                final BrushingLog finalRejected = latestRejected;
                final BrushingLog finalFeedback = latestFeedback;
                
                runOnUiThread(() -> {
                    if (finalRejected != null) {
                        rejectionReasonText.setText("Please try again. Reason: " + finalRejected.doctorFeedback);
                        rejectionCard.setVisibility(View.VISIBLE);
                    } else {
                        rejectionCard.setVisibility(View.GONE);
                    }
                    
                    if (finalFeedback != null) {
                        feedbackText.setText(finalFeedback.doctorFeedback);
                        feedbackCard.setVisibility(View.VISIBLE);
                    } else {
                        feedbackCard.setVisibility(View.GONE);
                    }
                });
            } catch (Exception e) {
                Log.e("ChildDashboard", "Log sync failed", e);
            }
            
            refreshDailyProgress();
        });
    }

    private void updateChildUI(User user) {
        welcomeText.setText("Hi, " + user.name + "!");
        if (streakText != null) {
            String streakDisplay = (user.streak % 1 == 0) ? String.format(Locale.getDefault(), "%.0f", user.streak) : String.format(Locale.getDefault(), "%.1f", user.streak);
            streakText.setText(streakDisplay + " Days");
        }
        
        if (user.warningNote != null && !user.warningNote.isEmpty()) {
            warningText.setText(user.warningNote);
            warningCard.setVisibility(View.VISIBLE);
        } else {
            warningCard.setVisibility(View.GONE);
        }

        // Update Rewards Visibility based on points
        updateRewardsUI(user.points);
    }

    private void updateRewardsUI(int points) {
        runOnUiThread(() -> {
            // Colors from colors.xml
            int lockedColor = 0xFFE0E0E0; // Grey
            int starColor = 0xFFFFD54F; // Yellow
            int pensColor = 0xFFF06292; // Pink
            int teddyColor = 0xFFBA68C8; // Purple
            int trophyColor = 0xFF4FC3F7; // Blue

            // Reward 1: Star (100 pts)
            if (points >= 100) {
                r1Card.setCardBackgroundColor(starColor);
                r1Check.setVisibility(View.VISIBLE);
            } else {
                r1Card.setCardBackgroundColor(lockedColor);
                r1Check.setVisibility(View.GONE);
            }

            // Reward 2: Pens (200 pts)
            if (points >= 200) {
                r2Card.setCardBackgroundColor(pensColor);
                r2Check.setVisibility(View.VISIBLE);
            } else {
                r2Card.setCardBackgroundColor(lockedColor);
                r2Check.setVisibility(View.GONE);
            }

            // Reward 3: Teddy (300 pts)
            if (points >= 300) {
                r3Card.setCardBackgroundColor(teddyColor);
                r3Check.setVisibility(View.VISIBLE);
            } else {
                r3Card.setCardBackgroundColor(lockedColor);
                r3Check.setVisibility(View.GONE);
            }

            // Reward 4: Trophy (500 pts)
            if (points >= 500) {
                r4Card.setCardBackgroundColor(trophyColor);
                r4Check.setVisibility(View.VISIBLE);
            } else {
                r4Card.setCardBackgroundColor(lockedColor);
                r4Check.setVisibility(View.GONE);
            }
        });
    }

    private void refreshDailyProgress() {
        Calendar cal = Calendar.getInstance();
        cal.set(Calendar.HOUR_OF_DAY, 0);
        cal.set(Calendar.MINUTE, 0);
        cal.set(Calendar.SECOND, 0);
        cal.set(Calendar.MILLISECOND, 0);
        long startOfDay = cal.getTimeInMillis();
        
        cal.set(Calendar.HOUR_OF_DAY, 23);
        cal.set(Calendar.MINUTE, 59);
        cal.set(Calendar.SECOND, 59);
        cal.set(Calendar.MILLISECOND, 999);
        long endOfDay = cal.getTimeInMillis();

        List<BrushingLog> logsToday = db.appDao().getBrushingLogsForChildToday(userId, startOfDay, endOfDay);
        int sessionsDone = logsToday != null ? logsToday.size() : 0;

        runOnUiThread(() -> {
            if (taskProgressBar != null) {
                taskProgressBar.setMax(2);
                taskProgressBar.setProgress(Math.min(sessionsDone, 2));
            }
            if (taskStatusText != null) {
                if (sessionsDone == 0) taskStatusText.setText("0/2 sessions completed today (0/10 pts)");
                else if (sessionsDone == 1) taskStatusText.setText("1/2 sessions completed today (+5 pts earned!)");
                else taskStatusText.setText("2/2 sessions completed today! (+10 pts max earned 🎉)");
            }
        });
    }

    @Override
    protected void onResume() {
        super.onResume();
        loadUserData();
    }
}
