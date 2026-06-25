import { useEffect, useState } from "react";

import { getCurrentUser } from "../api/authApi";

import type { User } from "../types/auth";

const useProfile = () => {
  const [user, setUser] = useState<User | null>(null);

  const [loading, setLoading] = useState(true);

  const [error, setError] = useState("");

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const data = await getCurrentUser();

        setUser(data);
      } catch {
        setError("Failed to load profile");
      } finally {
        setLoading(false);
      }
    };

    fetchUser();
  }, []);

  return {
    user,

    loading,

    error,
  };
};

export default useProfile;
