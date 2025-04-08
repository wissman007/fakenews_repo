resource "google_compute_firewall" "allow_airflow" {
  name    = "allow-airflow"
  network = "default"

  allow {
    protocol = "tcp"
    ports    = ["8080", "5000"]
  }

  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["airflow"]
}
