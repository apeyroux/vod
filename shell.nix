with import <nixpkgs>{};

let
  vod = (callPackage ./default.nix {});
in ((pkgs.python3.withPackages (ps: [ ps.celery vod ])).override {
  ignoreCollisions = true;
}).env
