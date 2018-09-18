{ pkgs, ... }:

with import <nixpkgs> {};

let

  vod = (callPackage ../default.nix {});

  py = ((pkgs.python3.withPackages (ps: [ ps.celery vod ])).override {
    ignoreCollisions = true;
  });
  
  vod-cfg = ''
ELASTICSEARCH_URL="http://127.0.0.1:9200"
CELERY_RESULT_BACKEND="redis://127.0.0.1:6379"
CELERY_BROKER_URL="redis://127.0.0.1:6379"
  '';

in rec {

  networking.firewall.allowedTCPPorts = [ 8080 ];

  services.redis =  {
    enable = true;
  };

  users.users.vod = {
    isNormalUser = true;
  };

  systemd.services.vod-worker = {
    enable =  true;
    environment = {};
    description = "Start vod-worker.";
    wantedBy = [ "default.target" ];
    serviceConfig = {
      User = "vod";
      ExecStart = "${py}/bin/celery -A vod.celery worker";
    };
  };

  systemd.services.vod-front = {
    enable =  true;
    environment = {};
    description = "Start vod-front.";
    wantedBy = [ "default.target" ];
    serviceConfig = {
      User = "vod";
      ExecStart = "${py}/bin/vod -l 0.0.0.0 -p 8080 --start";
    };
  };

}
