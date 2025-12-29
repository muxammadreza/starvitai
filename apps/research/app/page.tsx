"use client";

import { Button } from "@starvit/ui";

import styles from "../styles/index.module.css";
import { AuthGuard } from "./components/AuthGuard";

export default function Web() {
  return (
    <AuthGuard>
      <div className={styles.container}>
        <h1>Web</h1>
        <Button onClick={() => console.log("Pressed!")} text="Boop" />
      </div>
    </AuthGuard>
  );
}
