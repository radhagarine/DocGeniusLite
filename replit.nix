{pkgs}: {
  deps = [
    pkgs.libxcrypt
    pkgs.pango
    pkgs.harfbuzz
    pkgs.glib
    pkgs.ghostscript
    pkgs.fontconfig
  ];
}
