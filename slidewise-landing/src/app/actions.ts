"use server";

import { createClient } from "@supabase/supabase-js";

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

export async function joinWaitlist(
  email: string
): Promise<{ success: boolean; message: string }> {
  if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    return { success: false, message: "Please enter a valid email address." };
  }

  try {
    const { error } = await supabase.from("waitlist").insert([{ email }]);

    if (error) {
      if (error.code === "23505") {
        return {
          success: true,
          message: "You're already on the list. We'll be in touch.",
        };
      }
      throw error;
    }

    return {
      success: true,
      message: "You're in. We'll email you when it's ready.",
    };
  } catch {
    return { success: false, message: "Something went wrong. Please try again." };
  }
}
