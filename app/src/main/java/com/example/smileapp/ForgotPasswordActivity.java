package com.example.smileapp;

import android.os.Bundle;
import android.text.TextUtils;
import android.view.View;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import com.google.android.material.button.MaterialButton;
import com.google.android.material.textfield.TextInputEditText;

public class ForgotPasswordActivity extends AppCompatActivity {

    private TextInputEditText emailEditText;
    private MaterialButton resetLinkButton;
    private TextView backToLoginText;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_forgot_password);

        emailEditText = findViewById(R.id.email_edit_text);
        resetLinkButton = findViewById(R.id.reset_button);
        backToLoginText = findViewById(R.id.back_to_login);

        resetLinkButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String email = emailEditText.getText().toString().trim();

                if (TextUtils.isEmpty(email)) {
                    Toast.makeText(ForgotPasswordActivity.this, "Please enter your email", Toast.LENGTH_SHORT).show();
                    return;
                }

                resetLinkButton.setEnabled(false);

                new Thread(() -> {
                    boolean success = SupabaseAuthHelper.resetPasswordBlocking(email);
                    runOnUiThread(() -> {
                        resetLinkButton.setEnabled(true);
                        if (success) {
                            Toast.makeText(ForgotPasswordActivity.this, "Reset link sent to your email", Toast.LENGTH_LONG).show();
                            finish();
                        } else {
                            Toast.makeText(ForgotPasswordActivity.this, "Error: Failed to send reset link. Please check your email and try again.", Toast.LENGTH_LONG).show();
                        }
                    });
                }).start();
            }
        });

        backToLoginText.setOnClickListener(v -> finish());
    }
}
