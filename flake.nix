# Requires the following in ~/.config/nix/nix.conf
#   access-tokens = github.com=ghp_xxxx
{
  description = "edi_835_parser Nix Flake";

  inputs = {
    nixpkgs = {
      url = "github:NixOS/nixpkgs/nixos-unstable";
    };
    flake-utils = {
      url = "github:numtide/flake-utils";
    };
  };

  outputs = { self, nixpkgs, flake-utils, ... }:

    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
          config = { };
        };
      in
      {
        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            python311
            poetry
          ];
          shellHook = ''
            export TOP_DIR=$(pwd)
            export PATH=$PATH:$TOP_DIR/bin
            export PYTHONBREAKPOINT="ipdb.set_trace"
          '';
        };
      }
    );
}
