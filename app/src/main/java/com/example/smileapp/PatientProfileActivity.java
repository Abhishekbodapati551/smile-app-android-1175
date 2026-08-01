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
        
        if ("present".equals(status)) {
            showPrescriptionDialogAndMarkPresent();
        } else {
            executeAttendanceUpdate("absent", null);
        }
    }

    private void showPrescriptionDialogAndMarkPresent() {
        android.widget.LinearLayout layout = new android.widget.LinearLayout(this);
        layout.setOrientation(android.widget.LinearLayout.VERTICAL);
        layout.setPadding(40, 20, 40, 10);

        final android.widget.EditText diagInput = new android.widget.EditText(this);
        diagInput.setHint("Diagnosis (e.g. Routine Checkup)");
        layout.addView(diagInput);

        final android.widget.EditText medsInput = new android.widget.EditText(this);
        medsInput.setHint("Medicines (e.g. Fluoride Gel)");
        layout.addView(medsInput);

        final android.widget.EditText instInput = new android.widget.EditText(this);
        instInput.setHint("Instructions (e.g. Brush 2x daily)");
        layout.addView(instInput);

        new androidx.appcompat.app.AlertDialog.Builder(this)
                .setTitle("Issue Rx Prescription")
                .setMessage("Enter prescription details for this appointment:")
                .setView(layout)
                .setPositiveButton("Issue Rx & Save", (dialog, which) -> {
                    String diagnosis = diagInput.getText().toString().trim();
                    String medicines = medsInput.getText().toString().trim();
                    String instructions = instInput.getText().toString().trim();

                    if (diagnosis.isEmpty()) diagnosis = "Standard Checkup & Routine Hygiene";
                    if (medicines.isEmpty()) medicines = "No oral medicines prescribed.";
                    if (instructions.isEmpty()) instructions = "Maintain regular brushing 2x daily.";

                    try {
                        org.json.JSONObject rxJson = new org.json.JSONObject();
                        rxJson.put("diagnosis", diagnosis);
                        rxJson.put("medicines", medicines);
                        rxJson.put("instructions", instructions);
                        rxJson.put("issued_at", System.currentTimeMillis());
                        
                        executeAttendanceUpdate("present", rxJson.toString());
                    } catch (Exception e) {
                        executeAttendanceUpdate("present", null);
                    }
                })
                .setNegativeButton("Mark Present Only", (dialog, which) -> executeAttendanceUpdate("present", null))
                .setNeutralButton("Cancel", null)
                .show();
    }

    private void executeAttendanceUpdate(String status, String rxNotes) {
        if (activeAppt == null) return;
        activeAppt.status = status;
        activeAppt.prescriptionNotes = rxNotes;

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
                    SupabaseAuthHelper.updateWarningNoteBlocking(patientUid, null);
                }

                runOnUiThread(() -> {
                    Toast.makeText(this, "Marked " + status + (rxNotes != null ? " with Prescription 📋" : ""), Toast.LENGTH_SHORT).show();
                    attendanceTitle.setVisibility(View.GONE);
                    attendanceCard.setVisibility(View.GONE);
                    loadPatientData();
                });
            }
        }).start();
    }

    private void loadPatientData() {
        if (patientUid == null) return;
        SupabaseManager.execute(() -> {
            // 1. Show local patient data instantly
            User localPatient = db.appDao().getUserById(patientUid);
            List<BrushingLog> localLogs = db.appDao().getBrushingLogsForChild(patientUid);

            if (specificApptId != -1) {
                activeAppt = null;
                List<Appointment> allAppts = db.appDao().getAppointmentsForChild(patientUid);
                for (Appointment a : allAppts) if (a.id == specificApptId) { activeAppt = a; break; }
            }

            runOnUiThread(() -> {
                if (localPatient != null) {
                    nameText.setText(localPatient.name);
                    emailText.setText(localPatient.email);
                    pointsText.setText("⭐ " + localPatient.points);
                    String streakDisplay = (localPatient.streak % 1 == 0) ? String.format(Locale.getDefault(), "%.0f", localPatient.streak) : String.format(Locale.getDefault(), "%.1f", localPatient.streak);
                    streakText.setText("🔥 " + streakDisplay);
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
                historyList.addAll(localLogs);
                adapter.notifyDataSetChanged();
            });

            // 2. Fetch fresh patient profile & points from Supabase in background
            try {
                User freshPatient = SupabaseAuthHelper.fetchUserByIdBlocking(patientUid);
                if (freshPatient != null) {
                    db.appDao().insertUser(freshPatient);
                    runOnUiThread(() -> {
                        nameText.setText(freshPatient.name);
                        emailText.setText(freshPatient.email);
                        pointsText.setText("⭐ " + freshPatient.points);
                        String streakDisplay = (freshPatient.streak % 1 == 0) ? String.format(Locale.getDefault(), "%.0f", freshPatient.streak) : String.format(Locale.getDefault(), "%.1f", freshPatient.streak);
                        streakText.setText("🔥 " + streakDisplay);
                    });
                }
            } catch (Exception e) {
                android.util.Log.e("PatientProfile", "Failed to refresh patient profile from Supabase", e);
            }

            // 3. Sync fresh brushing logs from Supabase
            try {
                List<BrushingLog> freshLogs = SupabaseAuthHelper.fetchBrushingLogsForChildBlocking(patientUid);
                db.appDao().clearBrushingLogsForChild(patientUid);
                for (BrushingLog l : freshLogs) db.appDao().insertBrushingLog(l);
                
                runOnUiThread(() -> {
                    historyList.clear();
                    historyList.addAll(freshLogs);
                    adapter.notifyDataSetChanged();
                });
            } catch (Exception e) {
                android.util.Log.e("PatientProfile", "Failed to refresh logs from Supabase", e);
            }
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
