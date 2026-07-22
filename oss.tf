resource "alicloud_oss_bucket" "tf_state" {
  bucket        = "cloud-native-shop-tfstate-${var.alicloud_account_id}"
  storage_class = "Standard"

  versioning {
    status = "Enabled"
  }

  server_side_encryption_rule {
    sse_algorithm = "AES256"
  }

  acl = "private"
}
