locals {
  excluded_files = length(local.include_list) > 0 ? toset([
    for srcFile in local.source_files :
    srcFile if contains(local.include_list, srcFile) == false
  ]) : []
  include_list = fileexists(format("%s/include.lst", var.prefix)) ? split("\n", file(format("%s/include.lst", var.prefix))) : []
  source_files = fileset(var.prefix, "**")
}

data "archive_file" "source" {
  excludes    = local.excluded_files
  output_path = format("/tmp/%s/archive.%s", var.name, var.type)
  source_dir  = abspath(var.prefix)
  type        = "zip"
}
