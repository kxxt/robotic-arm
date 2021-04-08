import os

package_name = 'robotic-arm'
name = package_name
desp = 'Robotic Arm Application'
version = input('Please input version:')
package_path = f'{package_name}_{version}'
files_path = f'{package_path}/opt/robotic-arm/'
os.makedirs(files_path, exist_ok=True)
os.system(f'mkdir -p {package_path}/DEBIAN/')
os.system(f'mkdir -p {package_path}/usr/bin/')
os.system(f'cp -r ../src/** {files_path}')
os.system(f'cp *-robotic-arm {package_path}/usr/bin/')
os.system(f"cp {package_name}.service {package_path}/etc/systemd/system/")
os.system(f'cp preinst.sh {package_path}/DEBIAN/preinst')
os.system(f'cp prerm.sh {package_path}/DEBIAN/prerm')
os.system(f'cp postinst.sh {package_path}/DEBIAN/postinst')
os.makedirs(f"{package_path}/DEBIAN", exist_ok=True)
control_content = f'''Package: {package_name}
Architecture: all
Name: {name}
Description: {desp}
Version: {version}
Section: base
Depends: python3
Author: Robotic Arm Development Team <example@example.com>
Maintainer: Robotic Arm Development Team <example@example.com>
HomePage: https://github.com/USER/{package_name}
'''
ctl_file = open(f'{package_path}/DEBIAN/control', mode='w+')
ctl_file.write(control_content)
ctl_file.close()
for r, d, f in os.walk(package_path):
    os.chmod(r, 0o755)
os.system(f'chmod +x {package_path}/DEBIAN/*')
os.system(f'chmod +x {package_path}/usr/bin/*-robotic-arm')
os.system(f'dpkg-deb -b {package_path}')
