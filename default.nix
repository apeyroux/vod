{}:

with import <nixpkgs> {};

let
  req = (import ./requirements.nix { inherit pkgs; });
in python36Packages.buildPythonPackage  rec {
  pname = "vod";
  version = "1.0";
  src = ./.;
  buildInputs = builtins.attrValues req.packages;
  propagatedBuildInputs = builtins.attrValues req.packages;
  extraLibs = builtins.attrValues req.packages;
}
