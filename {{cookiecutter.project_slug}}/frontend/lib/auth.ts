import { NextAuthOptions } from "next-auth";
import CredentialsProvider from "next-auth/providers/credentials";
import FacebookProvider from "next-auth/providers/facebook";
import GoogleProvider from "next-auth/providers/google";

declare module "next-auth" {
  interface Session {
    user: {
      id: string;
      name: string;
      email: string;
      access_token: string;
      provider: string;
      role: string;
    };
  }

  interface User {
    id: string;
    name: string;
    email: string;
    access_token: string;
    provider: string;
    role: string;
  }
}

const SECRET_KEY = process.env.SECRET_KEY ?? "";
if (!SECRET_KEY) {
  throw new Error("SECRET_KEY is not defined in environment variables");
}

export const authConfig: NextAuthOptions = {
  providers: [
    CredentialsProvider({
      name: "Sign in",
      credentials: {
        email: {
          label: "Email",
          type: "email",
          placeholder: "user@example.com",
        },
        password: { label: "Password", type: "password" },
      },
      async authorize(credentials) {
        if (!credentials?.email || !credentials?.password) return null;
        try {
          const res = await fetch("http://backend:8000/api/django/login/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              email: credentials.email,
              password: credentials.password,
            }),
          });

          if (!res.ok) {
            const errorData = await res.json();
            throw new Error(errorData.detail || "Échec de la connexion");
          }

          const user = await res.json();
          return {
            id: user.id,
            name: user.username,
            email: user.email,
            access_token: user.access_token,
            provider: user.provider,
            role: "user",
          };
        } catch (error) {
          console.error("Login failed:", error);
          return null;
        }
      },
    }),
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID ?? "",
      clientSecret: process.env.GOOGLE_CLIENT_SECRET ?? "",
    }),
    FacebookProvider({
      clientId: process.env.FACEBOOK_CLIENT_ID ?? "",
      clientSecret: process.env.FACEBOOK_CLIENT_SECRET ?? "",
    }),
  ],
  callbacks: {
    async signIn({ user, account, profile }) {
      try {
        if (!account) {
          console.error("Erreur : 'account' est null ou undefined.");
          return false;
        }

        if (account.provider !== "credentials" && !profile) {
          console.error(
            `Erreur : 'profile' est null ou undefined pour le provider ${account.provider}.`
          );
          return false;
        }

        if (account.provider === "google" || account.provider === "facebook") {
          const googleId =
            account.provider === "google"
              ? (profile as { sub?: string })?.sub ?? null
              : null;
          const facebookId =
            account.provider === "facebook"
              ? (profile as { id?: string })?.id ?? null
              : null;

          const email = user.email ?? profile?.email ?? "";
          const name = user.name ?? profile?.name ?? "Utilisateur";

          if (!email) {
            console.error(
              "Erreur : Impossible d'extraire l'email de l'utilisateur."
            );
            return false;
          }

          const registerRes = await fetch(
            "http://backend:8000/api/django/register/",
            {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({
                email,
                name,
                google_id: googleId,
                facebook_id: facebookId,
                id: user.id ?? "",
              }),
            }
          );

          if (!registerRes.ok) {
            const registerData = await registerRes.json();
            console.error(
              "Erreur lors de l'enregistrement :",
              registerData.detail
            );
            return false;
          }
        }
      } catch (error) {
        console.error("Erreur dans le processus d'inscription :", error);
        return false;
      }
      return true;
    },

    async jwt({ token, user, account, trigger, session }) {
      // Premier cas : au moment du login
      if (user) {
        token.access_token = user.access_token;
        token.name = user.name;
        token.id = user.id;
        token.role = "user";
        token.provider = account?.provider ?? "credentials";
      }
      if (trigger === "update" && session) {
        if (session.name) token.name = session.name;
        if (session.email) token.email = session.email;
      }

      return token;
    },

    async session({ session, token }) {
      session.user.id = token.id as string;
      session.user.name = token.name as string;
      session.user.access_token = token.access_token as string;
      session.user.role = token.role as string;
      session.user.provider = token.provider as string;
      session.user.email = token.email as string;
      return session;
    },

    async redirect({ baseUrl }) {
      return baseUrl;
    },
  },
  secret: process.env.NEXTAUTH_SECRET,
};
