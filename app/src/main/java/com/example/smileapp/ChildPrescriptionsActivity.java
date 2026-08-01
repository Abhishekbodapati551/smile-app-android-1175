package com.example.smileapp;

import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageButton;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import com.example.smileapp.database.AppDatabase;
import com.example.smileapp.models.Appointment;

import org.json.JSONObject;

import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.Locale;

public class ChildPrescriptionsActivity extends AppCompatActivity {

    private static final String TAG = "ChildPrescriptions";
    private AppDatabase db;
    private String userId;
    private RecyclerView recyclerView;
    private View emptyContainer;
    private PrescriptionsAdapter adapter;
    private List<Appointment> prescriptionAppts = new ArrayList<>();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_child_prescriptions);

        db = AppDatabase.getInstance(this);
        userId = getIntent().getStringExtra("USER_ID");

        ImageButton backBtn = findViewById(R.id.back_button);
        if (backBtn != null) backBtn.setOnClickListener(v -> finish());

        emptyContainer = findViewById(R.id.empty_prescriptions_container);
        recyclerView = findViewById(R.id.prescriptions_recycler_view);

        recyclerView.setLayoutManager(new LinearLayoutManager(this));
        adapter = new PrescriptionsAdapter(prescriptionAppts);
        recyclerView.setAdapter(adapter);

        loadPrescriptions();
    }

    private void loadPrescriptions() {
        if (userId == null) {
            Toast.makeText(this, "User ID missing", Toast.LENGTH_SHORT).show();
            finish();
            return;
        }

        SupabaseManager.execute(() -> {
            // 1. Load local appointments with prescription notes
            List<Appointment> localAppts = db.appDao().getAllAppointmentsForChild(userId);
            List<Appointment> initialRxList = filterPrescriptions(localAppts);

            runOnUiThread(() -> updateUI(initialRxList));

            // 2. Refresh appointments from Supabase
            try {
                List<Appointment> freshAppts = SupabaseAuthHelper.fetchAppointmentsForChildBlocking(userId);
                for (Appointment a : freshAppts) {
                    db.appDao().insertAppointment(a);
                }

                List<Appointment> finalRxList = filterPrescriptions(freshAppts);
                runOnUiThread(() -> updateUI(finalRxList));
            } catch (Exception e) {
                Log.e(TAG, "Failed to refresh prescriptions from Supabase", e);
            }
        });
    }

    private List<Appointment> filterPrescriptions(List<Appointment> appts) {
        List<Appointment> result = new ArrayList<>();
        if (appts == null) return result;
        for (Appointment a : appts) {
            if (a.prescriptionNotes != null && !a.prescriptionNotes.trim().isEmpty()) {
                result.add(a);
            }
        }
        return result;
    }

    private void updateUI(List<Appointment> list) {
        prescriptionAppts.clear();
        prescriptionAppts.addAll(list);
        adapter.notifyDataSetChanged();

        if (emptyContainer != null && recyclerView != null) {
            if (prescriptionAppts.isEmpty()) {
                emptyContainer.setVisibility(View.VISIBLE);
                recyclerView.setVisibility(View.GONE);
            } else {
                emptyContainer.setVisibility(View.GONE);
                recyclerView.setVisibility(View.VISIBLE);
            }
        }
    }

    private static class PrescriptionsAdapter extends RecyclerView.Adapter<PrescriptionsAdapter.ViewHolder> {
        private final List<Appointment> list;

        public PrescriptionsAdapter(List<Appointment> list) {
            this.list = list;
        }

        @NonNull
        @Override
        public ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
            View view = LayoutInflater.from(parent.getContext()).inflate(R.layout.item_prescription, parent, false);
            return new ViewHolder(view);
        }

        @Override
        public void onBindViewHolder(@NonNull ViewHolder holder, int position) {
            Appointment appt = list.get(position);

            SimpleDateFormat sdf = new SimpleDateFormat("MMM dd, yyyy 'at' hh:mm a", Locale.getDefault());
            holder.dateText.setText(sdf.format(new Date(appt.date)));

            String notesStr = appt.prescriptionNotes;
            String clinicName = "Smile App Dental Clinic";
            String doctorName = "Dr. Dental Specialist";
            String diagnosis = "Routine Hygiene & Checkup";
            String medicines = "No oral medicines prescribed.";
            String instructions = "Maintain regular brushing 2x daily.";

            if (notesStr != null && !notesStr.isEmpty()) {
                try {
                    JSONObject json = new JSONObject(notesStr);
                    if (json.has("clinic_name")) clinicName = json.optString("clinic_name", clinicName);
                    if (json.has("doctor_name")) doctorName = "Dr. " + json.optString("doctor_name", doctorName);
                    if (json.has("diagnosis")) diagnosis = json.optString("diagnosis", diagnosis);
                    if (json.has("medicines")) medicines = json.optString("medicines", medicines);
                    if (json.has("instructions")) instructions = json.optString("instructions", instructions);
                } catch (Exception e) {
                    // Plain text fallback
                    diagnosis = notesStr;
                }
            }

            holder.clinicNameText.setText(clinicName);
            holder.doctorNameText.setText(doctorName);
            holder.diagnosisText.setText(diagnosis);
            holder.medicinesText.setText(medicines);
            holder.instructionsText.setText(instructions);
        }

        @Override
        public int getItemCount() {
            return list.size();
        }

        static class ViewHolder extends RecyclerView.ViewHolder {
            TextView dateText, clinicNameText, doctorNameText;
            TextView diagnosisText, medicinesText, instructionsText;

            public ViewHolder(@NonNull View v) {
                super(v);
                dateText = v.findViewById(R.id.rx_date);
                clinicNameText = v.findViewById(R.id.rx_clinic_name);
                doctorNameText = v.findViewById(R.id.rx_doctor_name);
                diagnosisText = v.findViewById(R.id.rx_diagnosis);
                medicinesText = v.findViewById(R.id.rx_medicines);
                instructionsText = v.findViewById(R.id.rx_instructions);
            }
        }
    }
}
