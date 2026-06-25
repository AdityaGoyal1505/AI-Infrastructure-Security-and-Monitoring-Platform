/* eslint-disable @typescript-eslint/no-explicit-any */
/* eslint-disable react-refresh/only-export-components */
/* eslint-disable react-hooks/set-state-in-effect */
import { createContext, useContext, useEffect, useState } from "react";

const AuthContext = createContext<any>(null);

export const AuthProvider = ({ children }: any) => {

  const [user, setUser] = useState(null);

  useEffect(() => {

    const storedUser = localStorage.getItem("user");

    if (storedUser) {

      setUser(

        JSON.parse(storedUser)

      );

    }

  }, []);

  const login = (data: any) => {

    setUser(data.user);

    localStorage.setItem(

      "user",

      JSON.stringify(data.user)

    );

  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem("user");
  };

  return (

    <AuthContext.Provider

      value={{
        user,
        login,
        logout,
        isAuthenticated: !!user,
      }}
    >

      {children}

    </AuthContext.Provider>

  );

};

export const useAuth = () => {

  return useContext(AuthContext);

};