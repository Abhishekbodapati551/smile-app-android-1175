package com.example.smileapp.models

import androidx.room.Entity
import androidx.room.PrimaryKey
import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable
import kotlinx.serialization.Transient

@Serializable
@Entity(tableName = "users")
data class User(
    @SerialName("id")
    @PrimaryKey
    @JvmField var uid: String = "",
    
    @JvmField var name: String = "",
    @JvmField var email: String = "",
    
    @Transient
    @JvmField var password: String = "",
    @JvmField var role: String = "",
    
    @SerialName("doctor_id")
    @JvmField var doctorId: String? = null,
    
    @SerialName("is_approved")
    @JvmField var isApproved: Boolean = false,
    
    @SerialName("clinic_name")
    @JvmField var clinicName: String? = null,
    
    @SerialName("specialization")
    @JvmField var specialization: String? = null,

    @JvmField var points: Int = 0,
    @JvmField var streak: Double = 0.0,
    @JvmField var stars: Int = 0,

    @SerialName("warning_note")
    @JvmField var warningNote: String? = null
) {
    // Constructor for Java compatibility
    constructor(uid: String, name: String, email: String, pass: String, role: String) : this(
        uid = uid,
        name = name,
        email = email,
        password = pass,
        role = role
    )
}
