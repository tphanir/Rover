{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  name = "pyopengl-env";

  buildInputs = with pkgs; [
    python3
		python3Packages.pillow
		python3Packages.tkinter
    python3Packages.pygame
    python3Packages.pyopengl
    python3Packages.pyserial
  ];
}

