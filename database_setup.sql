-- MASTER SQL SCRIPT FOR SMILE APP
-- Copy and run this in Supabase SQL Editor to initialize the database

-- 1. CLEAN RESET
DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
DROP FUNCTION IF EXISTS public.handle_new_user();
DROP FUNCTION IF EXISTS public.approve_and_reward();
DROP TABLE IF EXISTS public.appointments CASCADE;
DROP TABLE IF EXISTS public.brushing_logs CASCADE;
DROP TABLE IF EXISTS public.profiles CASCADE;
DROP SEQUENCE IF EXISTS doctor_id_seq;

-- 2. DOCTOR ID GENERATOR
CREATE SEQUENCE doctor_id_seq START 1176;

-- 3. PROFILES TABLE
CREATE TABLE public.profiles (
  id uuid REFERENCES auth.users NOT NULL PRIMARY KEY,
  name text, email text, role text, doctor_id text, clinic_name text,
  is_approved boolean DEFAULT false, points int DEFAULT 0, streak int DEFAULT 0, stars int DEFAULT 0
);

-- 4. BRUSHING LOGS TABLE
CREATE TABLE public.brushing_logs (
  id SERIAL PRIMARY KEY, child_id uuid REFERENCES auth.users NOT NULL, child_name text,
  doctor_id text, video_url text, created_at bigint, approved boolean DEFAULT false,
  is_rejected boolean DEFAULT false, doctor_feedback text
);

-- 5. APPOINTMENTS TABLE
CREATE TABLE public.appointments (
  id SERIAL PRIMARY KEY, child_id uuid REFERENCES auth.users NOT NULL, child_name text,
  doctor_id text, appt_date bigint, type text, status text DEFAULT 'upcoming'
);

-- 6. REGISTRATION TRIGGER
CREATE OR REPLACE FUNCTION public.handle_new_user() RETURNS trigger AS $$
DECLARE v_role text; v_doc_id text;
BEGIN
  BEGIN
    v_role := COALESCE(new.raw_user_meta_data->>'role', 'child');
    IF v_role = 'doctor' THEN v_doc_id := nextval('doctor_id_seq')::text;
    ELSE v_doc_id := new.raw_user_meta_data->>'doctor_id'; END IF;
    INSERT INTO public.profiles (id, email, name, role, is_approved, doctor_id)
    VALUES (new.id, new.email, COALESCE(new.raw_user_meta_data->>'name', split_part(new.email, '@', 1)), v_role, (v_role = 'doctor'), v_doc_id)
    ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name, role = EXCLUDED.role, doctor_id = EXCLUDED.doctor_id;
  EXCEPTION WHEN OTHERS THEN RETURN new; END;
  RETURN new;
END; $$ LANGUAGE plpgsql SECURITY DEFINER;
CREATE TRIGGER on_auth_user_created AFTER INSERT ON auth.users FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

-- 7. APPROVAL POWER FUNCTION
CREATE OR REPLACE FUNCTION public.approve_and_reward(p_log_id int, p_feedback text, p_points_to_add int) RETURNS void AS $$
DECLARE v_child_id uuid;
BEGIN
  SELECT child_id INTO v_child_id FROM public.brushing_logs WHERE id = p_log_id;
  UPDATE public.brushing_logs SET approved = true, is_rejected = false, doctor_feedback = p_feedback WHERE id = p_log_id;
  UPDATE public.profiles SET points = COALESCE(points, 0) + p_points_to_add, streak = COALESCE(streak, 0) + 1 WHERE id = v_child_id;
END; $$ LANGUAGE plpgsql SECURITY DEFINER;

-- 8. PERMISSIONS & REALTIME
ALTER TABLE public.profiles DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.brushing_logs DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.appointments DISABLE ROW LEVEL SECURITY;

-- Enable Realtime for these tables
ALTER TABLE public.profiles REPLICA IDENTITY FULL;
ALTER TABLE public.brushing_logs REPLICA IDENTITY FULL;
ALTER TABLE public.appointments REPLICA IDENTITY FULL;

BEGIN;
  DROP PUBLICATION IF EXISTS supabase_realtime;
  CREATE PUBLICATION supabase_realtime FOR TABLE public.profiles, public.brushing_logs, public.appointments;
COMMIT;

DROP POLICY IF EXISTS "Public Access" ON storage.objects;
CREATE POLICY "Public Access" ON storage.objects FOR ALL USING (true) WITH CHECK (true);
