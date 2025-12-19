// server/server.js
import express from "express";
import fs from "fs";
import path from "path";
import cors from "cors";

const app = express();
app.use(express.json());
app.use(cors());

const __dirname = process.cwd();
const dataDir = path.join(__dirname, "server", "data");
const csvPath = path.join(dataDir, "feedback.csv");

// Ensure folder + CSV exist
if (!fs.existsSync(dataDir)) fs.mkdirSync(dataDir, { recursive: true });
if (!fs.existsSync(csvPath))
  fs.writeFileSync(
    csvPath,
    "lesson_clear,engaged,respectful,doubts,timestamp\n",
    "utf8"
  );

function csvSafe(v) {
  if (!v) return "";
  return `"${String(v).replace(/"/g, '""')}"`;
}

app.post("/submit-feedback", (req, res) => {
  const { lessonClear, engaged, respectful, doubts } = req.body;

  if (!lessonClear || !engaged || !respectful) {
    return res.status(400).json({ success: false, message: "Missing fields" });
  }

  const timestamp = new Date().toISOString();
  const line =
    `${csvSafe(lessonClear)},${csvSafe(engaged)},${csvSafe(
      respectful
    )},${csvSafe(doubts)},${csvSafe(timestamp)}\n`;

  fs.appendFileSync(csvPath, line, "utf8");

  res.json({ success: true });
});

app.listen(4000, () => {
  console.log("Server running on http://localhost:4000");
});
