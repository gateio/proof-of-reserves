"name": "projem-devcontainer",
    "image": "mcr.microsoft.com/devcontainers/base:ubuntu", // Herhangi bir genel, debian tabanlı görüntü.
    "özellikler": {
        "ghcr.io/devcontainers/features/go:1": {
            "sürüm": "1.18"
        },
        "ghcr.io/devcontainers/features/docker-in-docker:1": {
            "sürüm": "en son",
            "moby": doğru
        }
    }
