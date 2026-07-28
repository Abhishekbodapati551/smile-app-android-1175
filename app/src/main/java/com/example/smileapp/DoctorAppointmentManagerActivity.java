package com.example.smileapp;

import android.app.DatePickerDialog;
import android.app.TimePickerDialog;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.AutoCompleteTextView;
import android.widget.ProgressBar;
import android.widget.TextView;
import android.widget.Toast;
import androidx.annotation.NonNull;
import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;
import com.example.smileapp.database.AppDatabase;
import com.example.smileapp.models.Appointment;
import com.example.smileapp.models.User;
import com.google.android.material.button.MaterialButton;
import com.google.android.material.textfield.TextInputEditText;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.List;
import java.util.Locale;

public class DoctorAppointmentManagerActivity extends AppCompatActivity {

    private AppDatabase db;
    private String doctorUid;
    private String sequentialDoctorId;
    private RecyclerView recyclerView;
    private AppointmentAdapter adapter;
    private ProgressBar mainProgress;
    private List<Appointment> appointmentList = new ArrayList<>();
    private List<User> myPatients = new ArrayList<>();

    private TextView totalMgmtText, confirmedMgmtText, pendingMgmtText;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_doctor_appointment_manager);

        db = AppDatabase.getInstance(this);
        doctorUid = getIntent().getStringExtra("USER_ID");

        totalMgmtText = findViewById(R.id.total_mgmt_text);
        confirmedMgmtText = findViewById(R.id.confirmed_mgmt_text);
        pendingMgmtText = findViewById(R.id.pending_mgmt_text);

        recyclerView = findViewById(R.id.appointments_recycler);
        recyclerView.setLayoutManager(new LinearLayoutManager(this));
        adapter = new AppointmentAdapter(appointmentList);
        recyclerView.setAdapter(adapter);
        mainProgress = findViewById(R.id.main_progress);

        findViewById(R.id.add_appointment_btn).setOnClickListener(v -> showAddAppointmentDialog());

        loadDoctorData();
    }

    private void loadDoctorData() {
        new Thread(() -> {
            User doctor = db.appDao().getUserById(doctorUid);
            if (doctor != null) {
                sequentialDoctorId = doctor.doctorId;
                loadPatients();
                loadAppointments();
            }
        }).start();
    }

    private void loadPatients() {
        if (sequentialDoctorId == null) return;
        new Thread(() -> myPatients = db.appDao().getPatientsByDoctor(sequentialDoctorId)).start();
    }

    private void loadAppointments() {
        if (sequentialDoctorId == null) return;
        runOnUiThread(() -> mainProgress.setVisibility(View.VISIBLE));
        SupabaseManager.execute(() -> {
            try {
                // 1. Fetch fresh appointments from Supabase
                List<Appointment> latestApps = SupabaseAuthHelper.fetchAppointmentsBlocking(sequentialDoctorId);
                
                // 2. Clear local table first to ensure we use Cloud IDs
                db.appDao().clearAllAppointments();
                for (Appointment a : latestApps) db.appDao().insertAppointment(a);

                runOnUiThread(() -> {
                    mainProgress.setVisibility(View.GONE);
                    appointmentList.clear();
                    appointmentList.addAll(latestApps);
                    adapter.notifyDataSetChanged();
                    updateAppointmentStatsUI(latestApps);
                });
            } catch (Exception e) {
                Log.e("AppointmentManager", "Fetch failed", e);
                // Fallback to local
                List<Appointment> apps = db.appDao().getAppointmentsForDoctor(sequentialDoctorId);
                runOnUiThread(() -> {
                    mainProgress.setVisibility(View.GONE);
                    appointmentList.clear();
                    appointmentList.addAll(apps);
                    adapter.notifyDataSetChanged();
                    updateAppointmentStatsUI(apps);
                });
            }
        });
    }

    private void updateAppointmentStatsUI(List<Appointment> apps) {
        int total = apps.size();
        int confirmed = 0;
        int pending = 0;

        for (Appointment a : apps) {
            String s = a.status != null ? a.status.toLowerCase() : "upcoming";
            if (s.equals("confirmed") || s.equals("present") || s.equals("completed")) {
                confirmed++;
            } else {
                pending++;
            }
        }

        if (totalMgmtText != null) totalMgmtText.setText(String.valueOf(total));
        if (confirmedMgmtText != null) confirmedMgmtText.setText(String.valueOf(confirmed));
        if (pendingMgmtText != null) pendingMgmtText.setText(String.valueOf(pending));
    }

    private void showAddAppointmentDialog() {
        if (myPatients.isEmpty()) {
            Toast.makeText(this, "No patients found.", Toast.LENGTH_SHORT).show();
            return;
        }

        AlertDialog.Builder builder = new AlertDialog.Builder(this);
        View view = LayoutInflater.from(this).inflate(R.layout.dialog_add_appointment, null);
        builder.setView(view);

        AutoCompleteTextView patientSpinner = view.findViewById(R.id.patient_selector);
        TextInputEditText typeEdit = view.findViewById(R.id.appointment_type_edit);
        TextView dateText = view.findViewById(R.id.selected_date_text);
        MaterialButton pickDateBtn = view.findViewById(R.id.pick_date_btn);

        final Calendar calendar = Calendar.getInstance();
        List<String> names = new ArrayList<>();
        for (User u : myPatients) names.add(u.name);
        patientSpinner.setAdapter(new ArrayAdapter<>(this, android.R.layout.simple_dropdown_item_1line, names));

        pickDateBtn.setOnClickListener(v -> {
            new DatePickerDialog(this, (v1, y, m, d) -> {
                calendar.set(y, m, d);
                new TimePickerDialog(this, (v2, h, min) -> {
                    calendar.set(Calendar.HOUR_OF_DAY, h);
                    calendar.set(Calendar.MINUTE, min);
                    dateText.setText(new SimpleDateFormat("MMM dd, yyyy - hh:mm a", Locale.getDefault()).format(calendar.getTime()));
                }, 10, 0, false).show();
            }, calendar.get(Calendar.YEAR), calendar.get(Calendar.MONTH), calendar.get(Calendar.DAY_OF_MONTH)).show();
        });

        builder.setPositiveButton("Schedule", (dialog, which) -> {
            String name = patientSpinner.getText().toString();
            String type = typeEdit.getText().toString().trim();
            User p = null;
            for (User u : myPatients) if (u.name.equals(name)) { p = u; break; }

            if (p != null && !type.isEmpty()) {
                Appointment app = new Appointment(p.uid, p.name, sequentialDoctorId, calendar.getTimeInMillis(), type);
                saveAppointment(app);
            }
        });
        builder.setNegativeButton("Cancel", null).show();
    }

    private void saveAppointment(Appointment app) {
        runOnUiThread(() -> mainProgress.setVisibility(View.VISIBLE));
        new Thread(() -> {
            boolean success;
            if (app.id > 0) {
                // Update existing appointment
                success = SupabaseAuthHelper.updateAppointmentBlocking(app);
            } else {
                // Insert new appointment
                success = SupabaseAuthHelper.saveAppointmentBlocking(app);
            }

            if (success) {
                db.appDao().insertAppointment(app);
                runOnUiThread(() -> {
                    Toast.makeText(this, app.id > 0 ? "Rescheduled!" : "Scheduled!", Toast.LENGTH_SHORT).show();
                    loadAppointments();
                });
            } else {
                runOnUiThread(() -> {
                    mainProgress.setVisibility(View.GONE);
                    Toast.makeText(this, "Failed to save appointment", Toast.LENGTH_SHORT).show();
                });
            }
        }).start();
    }

    private void showRescheduleDialog(Appointment app) {
        AlertDialog.Builder builder = new AlertDialog.Builder(this);
        View view = LayoutInflater.from(this).inflate(R.layout.dialog_add_appointment, null);
        builder.setView(view);

        TextView title = view.findViewById(R.id.dialog_title);
        if (title != null) title.setText("Reschedule Appointment");

        AutoCompleteTextView patientSpinner = view.findViewById(R.id.patient_selector);
        TextInputEditText typeEdit = view.findViewById(R.id.appointment_type_edit);
        TextView dateText = view.findViewById(R.id.selected_date_text);
        MaterialButton pickDateBtn = view.findViewById(R.id.pick_date_btn);

        // Pre-fill
        patientSpinner.setText(app.childName);
        patientSpinner.setEnabled(false); // Can't change patient while rescheduling
        typeEdit.setText(app.type);
        
        final Calendar calendar = Calendar.getInstance();
        calendar.setTimeInMillis(app.date);
        dateText.setText(new SimpleDateFormat("MMM dd, yyyy - hh:mm a", Locale.getDefault()).format(calendar.getTime()));

        pickDateBtn.setOnClickListener(v -> {
            new DatePickerDialog(this, android.R.style.Theme_DeviceDefault_Light_Dialog_Alert, (v1, y, m, d) -> {
                calendar.set(y, m, d);
                new TimePickerDialog(this, android.R.style.Theme_DeviceDefault_Light_Dialog_Alert, (v2, h, min) -> {
                    calendar.set(Calendar.HOUR_OF_DAY, h);
                    calendar.set(Calendar.MINUTE, min);
                    dateText.setText(new SimpleDateFormat("MMM dd, yyyy - hh:mm a", Locale.getDefault()).format(calendar.getTime()));
                }, calendar.get(Calendar.HOUR_OF_DAY), calendar.get(Calendar.MINUTE), false).show();
            }, calendar.get(Calendar.YEAR), calendar.get(Calendar.MONTH), calendar.get(Calendar.DAY_OF_MONTH)).show();
        });

        builder.setPositiveButton("Update", (dialog, which) -> {
            String type = typeEdit.getText().toString().trim();
            if (!type.isEmpty()) {
                app.type = type;
                app.date = calendar.getTimeInMillis();
                saveAppointment(app);
            }
        });
        builder.setNegativeButton("Cancel", null).show();
    }

    private class AppointmentAdapter extends RecyclerView.Adapter<AppointmentAdapter.ViewHolder> {
        private List<Appointment> apps;
        public AppointmentAdapter(List<Appointment> apps) { this.apps = apps; }
        @NonNull
        @Override
        public ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
            return new ViewHolder(LayoutInflater.from(parent.getContext()).inflate(R.layout.item_appointment, parent, false));
        }
        @Override
        public void onBindViewHolder(@NonNull ViewHolder holder, int position) {
            Appointment a = apps.get(position);
            holder.pName.setText(a.childName);
            holder.type.setText(a.type);
            holder.date.setText(new SimpleDateFormat("MMM dd, yyyy - hh:mm a", Locale.getDefault()).format(new Date(a.date)));
            holder.rescheduleBtn.setOnClickListener(v -> showRescheduleDialog(a));
        }
        @Override
        public int getItemCount() { return apps.size(); }
        class ViewHolder extends RecyclerView.ViewHolder {
            TextView pName, type, date;
            MaterialButton rescheduleBtn;
            public ViewHolder(@NonNull View v) {
                super(v);
                pName = v.findViewById(R.id.patient_name);
                type = v.findViewById(R.id.appointment_type);
                date = v.findViewById(R.id.appointment_date);
                rescheduleBtn = v.findViewById(R.id.reschedule_btn);
            }
        }
    }
}
