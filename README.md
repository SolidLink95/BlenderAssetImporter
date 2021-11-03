# Asset importer

Inspired by [this comment]([I need an addon developer for a freelance paid job - Jobs / Paid Work - Blender Artists Community](https://blenderartists.org/t/i-need-an-addon-developer-for-a-freelance-paid-job/1331305)) from [blenderartists.org](blenderartists.org) I created an addon for importing assets into blender scene using image preview. For now only png images are supported.

![alt text](https://github.com/banan039pl/BlenderAssetImporter/blob/main/images/1.png)

![alt text](https://github.com/banan039pl/BlenderAssetImporter/blob/main/images/4.png)

## Installation

In order to get the addon working download latest release (don't unzip it). In blender go to `Edit -> Preferences -> Add-ons -> Install...` and point to downloaded zip file. Enable it by ticking the box. From now Asset importer will be available in `Properties -> View layer`

![alt text](https://github.com/banan039pl/BlenderAssetImporter/blob/main/images/2.png)

![alt text](https://github.com/banan039pl/BlenderAssetImporter/blob/main/images/3.png)

The `Documentation` button redirects to this github page.

## Usage

1. Create a directory with all png files with previews of the assets, lets name the folder `previews`
2. Navigate to parent directory  of `previews` folder. Create `blends` folder and put your assets here. Supported extensions are:
   - *.blend
   - *.fbx
   - *.glb
   - *.dae
3. Images names in `previews` directory must be the same as assets in `blends` directory. Example: When I copy `SkeletonWarrior.png` to `previews` then I need to copy`SkeletonWarrior.blend` to `blends`. If there is no asset named `SkeletonWarrior` in `blends` folder the preview will not appear in blender.
4. The assets priority loading is just like written in 2. If there are `SkeletonWarrior.blend` and `SkeletonWarrior.fbx` in `blends` directory then `SkeletonWarrior.blend` will be loaded.
5. Click `Import assets` to load all assets to current scene

### Features

- after adding png file and asset file to respective folders there is no need to restart blender - just make sure `Filter` text field is empty and click `Filter`to reload
- any files in `previews` folder with extension other that `png` will be skipped

I recommend making png files around 128x128 to 512x512 in  order to save loading time of images.

## Credits

I used `ui_previews_dynamic_enum.py` template as a base for it. I modified an ui by adding filtering options. I also added some of my python functions I use on daily basis