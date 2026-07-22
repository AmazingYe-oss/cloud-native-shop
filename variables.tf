variable "alicloud_access_key" {
  type        = string
  description = "阿里云 AccessKey ID"
  sensitive   = true
}

variable "alicloud_secret_key" {
  type        = string
  description = "阿里云 AccessKey Secret"
  sensitive   = true
}

variable "alicloud_region" {
  type        = string
  description = "阿里云地域（默认用上海区）"
  default     = "cn-shanghai"
}

variable "alicloud_account_id" {
  type        = string
  description = "阿里云账号 ID（16 位数字）"
}
