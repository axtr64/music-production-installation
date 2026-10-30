# music production installation repository

*personal installation reference · linux · fedora*

this repository serves as a reference guide for installing and managing music production applications, audio plugins, effects, and supporting resources on fedora linux.

it covers music composition using lmms, recording and mixing through reaper and ardour, guitar processing with guitarix, vocal correction using snaptune, and audio management through easyeffects.

**installation note:** the commands provided are installation references. some applications use fedora packages, while others require downloading and installing their official linux releases. verify package availability and installation status before proceeding.

---
## **setup.py** is a python-based installation script designed to simplify the setup of a music production environment on fedora linux. it automatically checks whether the required applications, plugins, and audio utilities are already installed, then identifies and installs missing packages when available. it can also download and install snaptune from its official gitHub release and prepare the necessary LMMS asset folders.

*to use it, download the script, open a terminal in its directory, and run:*
``python3 setup.py --all``

- the script guides you through the installation process and asks for confirmation before making system changes. tt also provides options to check existing installations or install specific components separately.
- this script is useful when setting up the same music production environment on a fresh fedora installation or another compatible computer.
- the script will guide you through the installation. it asks for confirmation before installing fedora packages and before downloading and running the snaptune installer.

**command	purpose**
```python
python3 setup.py --check	// Check which software is installed
python3 setup.py --packages	// Install available Fedora packages
python3 setup.py --snaptune	// Install or update SnapTune
python3 setup.py --all	        // Run the complete setup
```

**what the automation handles**
- **installed software**: checks existing RPM packages and skips those already installed.
- **fedora packages**: installs available DAWs, plugins, audio utilities, and dependencies.
- **ardour**: checks both ardour9 and ardour package names.
- **snaptune**: retrieves the latest Linux release from its official github repository.
- **LMMS assets**: creates the drumkits, presets, samples, and soundfonts folders if missing.
- **REAPER**: provides the official download and installation instructions because it uses a separate installer.

**important:** this is designed for fedora linux on x86-64. some optional packages may not exist in your enabled repositories; the script reports and skips those rather than stopping the entire setup. it does not delete your existing plugins, soundfonts, or music projects.


---

## 1. music production applications

these applications are used for composing, recording, arranging, editing, and mixing music.

### 1.1 lmms

**description:** digital audio workstation for midi composition, virtual instruments, beat production, and musical arrangements.

- installation:
  ```bash
  sudo dnf install lmms
  ```
- launch:
  ```bash
  lmms
  ```

### 1.2 reaper

**description:** digital audio workstation for multitrack recording, audio editing, mixing, and mastering.

- installation:
  - visit the [reaper official download page](https://www.reaper.fm/download.php).
  - download the linux x86_64 version.
  - extract the downloaded archive.
  - enter the extracted directory and run:
    ```bash
    ./install-reaper.sh
    ```
- launch:
  ```bash
  reaper
  ```

### 1.3 ardour

**description:** multitrack audio recording and editing software for arranging, processing, and mixing audio.

- installation:
  ```bash
  sudo dnf install ardour9
  ```
- launch:
  ```bash
  ardour9
  ```

### 1.4 hydrogen

**description:** pattern-based drum machine for creating acoustic and electronic drum sequences.

- installation:
  ```bash
  sudo dnf install hydrogen
  ```
- launch:
  ```bash
  hydrogen
  ```

### 1.5 guitarix

**description:** virtual guitar amplifier and effects processor for creating electric guitar tones and applying amplifier effects.

- installation:
  ```bash
  sudo dnf install guitarix
  ```
- launch:
  ```bash
  guitarix
  ```

### 1.6 easyeffects

**description:** audio effects processor for managing microphone input and system output through equalizers, compressors, limiters, and other effects.

- installation:
  ```bash
  sudo dnf install easyeffects
  ```
- launch:
  ```bash
  easyeffects
  ```

---

## 2. installed plugins and audio effects

these plugins provide equalization, compression, reverb, pitch correction, guitar processing, and vocal effects inside compatible audio applications.

### 2.1 calf studio gear

**description:** collection of audio effects and instruments, including equalizers, compressors, reverbs, and limiters.

- installation:
  ```bash
  sudo dnf install calf lv2-calf-plugins
  ```

### 2.2 x42 plugins

**description:** audio plugin collection for metering, equalization, tuning, and signal processing.

- installation:
  ```bash
  sudo dnf install lv2-x42-plugins
  ```

### 2.3 autotalent

**description:** ladspa pitch correction effect for adjusting vocal pitch and tuning.

- installation:
  ```bash
  sudo dnf install ladspa-autotalent-plugins
  ```

### 2.4 snaptune 2.2.0

**description:** vocal pitch correction plugin with natural tuning, hard tuning, and formant control.

- installation:
  - download the linux archive from [snaptune releases](https://github.com/NicoFerni/snaptune/releases).
  - extract the downloaded archive.
  - enter the extracted directory and run:
    ```bash
    tar -xf SnapTune-2.2.0-Linux.tar.gz
    cd SnapTune-2.2.0-Linux
    chmod +x install.sh
    ./install.sh
    ```
- launch:
  ```bash
  ~/.local/bin/SnapTune
  ```
- plugin directories:
  - vst3: `~/.vst3/`
  - lv2: `~/.lv2/`
  - standalone application: `~/.local/bin/`

after installation, restart the daw and rescan its available plugins.

### 2.5 guitarix effects

**description:** guitar amplifier simulation and audio effects for processing electric guitar recordings.

- installation:
  ```bash
  sudo dnf install guitarix
  ```
- launch:
  ```bash
  guitarix
  ```

**plugin precaution:**
- verify that the daw supports the plugin format before installation.
- rescan the plugin directory after installing new vst3 or lv2 effects.
- remember that a standalone audio application and its plugins are not necessarily the same installation.

---

## 3. audio system and utilities

these applications and packages handle audio connections, routing, recording compatibility, and device management.

- **pipewire** – main linux audio and video processing service.
- **pipewire jack** – provides jack compatibility for professional audio applications.
- **pulseAudio volume control** – graphical interface for managing audio devices and volume.
- **qpwgraph** – graphical audio and midi connection manager.
- **fluidsynth** – software synthesizer for playing soundfont instruments.

### installation

```bash
sudo dnf install \
pipewire \
pipewire-alsa \
pipewire-jack-audio-connection-kit \
pavucontrol \
qpwgraph \
fluidsynth
```

### launch commands

- pulseAudio volume control:
  ```bash
  pavucontrol
  ```
- qpwgraph:
  ```bash
  qpwgraph
  ```
- fluidsynth:
  ```bash
  fluidsynth
  ```
- pipewire service status:
  ```bash
  systemctl --user status pipewire
  ```

**audio system precaution:**
- pipewire is already the default audio system on many fedora installations.
- avoid installing or configuring competing audio servers without a specific requirement.
- check audio device connections before starting recording sessions.
- use the appropriate jack compatibility configuration when working with professional audio applications.

---

## 4. lmms assets, soundfonts and drumkits

these are the sample libraries and instrument resources used by lmms and hydrogen to create realistic instruments, guitar sounds, bass, piano, and drum arrangements.

### 4.1 lmms assets

**description:** collection of samples, presets, drumkits, and soundfonts used for music composition and production.

- main directory:
  ```bash
  ~/Music/LMMS/LMMS-assets/
  ```

- expected folder structure:
  ```text
  LMMS-assets/
  ├── Drumkits/
  ├── Presets/
  ├── Samples/
  └── Soundfonts/
  ```

- create the directories:
  ```bash
  mkdir -p ~/Music/LMMS/LMMS-assets/{Drumkits,Presets,Samples,Soundfonts}
  ```

### 4.2 soundfonts (sf2)

**description:** soundfont instrument libraries containing sampled instruments such as piano, guitar, bass, strings, brass, and other general midi sounds.

- recommended soundfont: fluidr3 general midi.
- installation:
  ```bash
  sudo dnf install fluid-soundfont-gm fluid-soundfont-gs
  ```

- locate installed soundfonts:
  ```bash
  find /usr/share/soundfonts -type f
  ```

- alternative package file lookup:
  ```bash
  rpm -ql fluid-soundfont-gm | grep -i '\.sf2$'
  ```

- create the personal soundfont directory:
  ```bash
  mkdir -p ~/Music/LMMS/LMMS-assets/Soundfonts
  ```

- copy the selected `.sf2` file into the soundfonts directory.

### 4.3 hydrogen drumkits

**description:** sample-based acoustic and electronic drum libraries for creating realistic rhythm arrangements.

- installation:
  ```bash
  sudo dnf install hydrogen
  ```

- included drumkits:
  - gmrockkit – acoustic rock drum samples.
  - tr808emulationkit – electronic 808-style drum samples.

- default directory:
  ```bash
  /usr/share/hydrogen/data/drumkits/
  ```

- personal lmms drumkit directory:
  ```bash
  ~/Music/LMMS/LMMS-assets/Drumkits/
  ```

---

## 5. safety precautions and installation checklist

follow these precautions before installing, configuring, or launching music production applications.

### a. before installation

- check whether the application is already installed:
  ```bash
  command -v lmms reaper ardour9 hydrogen guitarix easyeffects
  ```
- verify the availability of a fedora package:
  ```bash
  dnf info ardour9
  ```
- use `dnf` for fedora packages instead of ubuntu's `apt` installation commands.
- download applications from official websites or trusted github releases.
- avoid installing unknown rpm packages or executing scripts from untrusted sources.
- verify the downloaded archive and its architecture before extracting or installing it.

### b. package installation precautions

- verify the correct package name before executing an installation command.
- install only the applications and plugins needed for your production workflow.
- avoid reinstalling packages that are already installed.
- read the terminal output before confirming an installation.
- if a package cannot be found, check its availability in the configured fedora repositories.
- do not substitute package names from tutorials written for other linux distributions.

### c. application launching precautions

- verify the executable before launching:
  ```bash
  command -v guitarix
  ```
- use the correct launch command for each application.
- for downloaded installers, navigate to the correct extracted directory first.
- make installer scripts executable when required:
  ```bash
  chmod +x install.sh
  ./install.sh
  ```
- do not use `sudo` for user-level installers unless the official installation instructions require it.
- if an application does not launch, check the terminal error message before attempting another installation.

### d. audio and plugin precautions

- use headphones when monitoring vocals to prevent microphone feedback.
- avoid running multiple audio servers or competing jack configurations.
- do not modify pipewire configuration files without understanding the changes.
- save daw projects before changing audio devices or audio routing.
- confirm the correct input and output devices before recording.
- rescan plugins after installing new vst3 or lv2 effects.
- check plugin compatibility with the daw before using an effect.

---

## 6. quick installation command repository

the following commands group the available fedora packages by their purpose. execute them individually according to your requirements.

### music production applications

```bash
sudo dnf install lmms ardour9 hydrogen guitarix easyeffects
```

### audio plugins and effects

```bash
sudo dnf install calf lv2-calf-plugins lv2-x42-plugins ladspa-autotalent-plugins
```

### audio system and utilities

```bash
sudo dnf install pipewire pipewire-alsa pipewire-jack-audio-connection-kit pavucontrol qpwgraph fluidsynth
```

### soundfonts

```bash
sudo dnf install fluid-soundfont-gm fluid-soundfont-gs
```

### lmms asset directories

```bash
mkdir -p ~/Music/LMMS/LMMS-assets/{Drumkits,Presets,Samples,Soundfonts}
```

**additional installation notes:**
- reaper requires its official linux installer.
- snaptune requires its downloaded linux installer.
- do not include these two applications in the fedora bulk installation command.
- check package availability before executing commands on a different fedora release.

---

## 7. official resources

- **lmms:** https://lmms.io/
- **reaper:** https://www.reaper.fm/
- **ardour:** https://ardour.org/
- **hydrogen:** http://www.hydrogen-music.org/
- **guitarix:** https://guitarix.org/
- **easyeffects:** https://github.com/wwmm/easyeffects
- **snaptune:** https://github.com/NicoFerni/snaptune
- **fedora packages:** https://packages.fedoraproject.org/

