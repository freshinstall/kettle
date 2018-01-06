# freshinstall

Freshinstall (working title) is a configuration backup-restore tool for Debian-based OSs like Pop_OS. It uses a standard file format to save data in the system and restore it to another system (or reinstallation). It can also be used for sharing standard configuration environments, such as a video editing setup, Node.js development, etc.

### File format
Freshinstall uses a standard file using the file extension `.fix`. Despite this, the file contains a standard lzma-compressed tar archive, which makes creating these files by hand very simple. The structure of a `.fix` file is below:
```
/
/data/
  /binary/
      /executable_file
  /repos/
    /apt_sources.list
    /extra_sources.list.d/
      /extra_source.list
  /packages/
    /extra_package.deb
  /src/
    /source_packages.tar
  /config/
    /etc/
      /system_configuration/
        /files
   /home
     /.personal/
       /dot_files
  /lists/
    /installed_pkg.list
    /removed_pkg.list
/scripts
  /extra_scripts_to_run.sh
/metainfo
  /meta.json
```
`.fix` files can contain extra packages that need to be installed, third-party repositories that need to be enabled, configuration files to set up custom options, source pacakges to include for manual installation, and scripts to run to perform other actions. 
