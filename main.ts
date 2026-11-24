// Menyalin gambar entry.png ke folder keluaran yang diminta make.fun.
// Gambar sudah dibuat sebelumnya dan tersimpan di samping berkas ini,
// jadi tugas program ini hanya memindahkannya ke tempat yang benar.

import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const folderSkrip = dirname(fileURLToPath(import.meta.url));
const folderTujuan = process.env.MAKEFUN_OUTPUT_DIR || "/output";

const jalurAsal = join(folderSkrip, "entry.png");
const jalurTujuan = join(folderTujuan, "entry.png");

// Siapkan folder tujuan dulu supaya penulisan tidak gagal
// ketika foldernya belum pernah dibuat.
mkdirSync(folderTujuan, { recursive: true });

const isiGambar = readFileSync(jalurAsal);
writeFileSync(jalurTujuan, isiGambar);

console.log(`entry.png sudah disalin ke ${jalurTujuan}`);
