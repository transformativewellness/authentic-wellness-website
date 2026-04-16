/**
 * Optional Supabase REST credentials for program waitlist signups.
 * Leave strings empty to store submissions in localStorage only until configured.
 * Create table program_enrollment_waitlist (id uuid default gen_random_uuid(), created_at timestamptz default now(), full_name text, email text, program_slug text) with RLS allowing anon INSERT.
 */
window.AW_PROGRAM_WAITLIST = window.AW_PROGRAM_WAITLIST || {
  supabaseUrl: "",
  supabaseAnonKey: "",
  tableName: "program_enrollment_waitlist",
};
