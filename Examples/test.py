from pprint import pprint
from python_get_resolve import GetResolve
from typing import List, Union
import sys

media_path: str = sys.argv[1]

resolve = GetResolve()
project_manager = resolve.GetProjectManager()
project = project_manager.GetCurrentProject()
media_storage = resolve.GetMediaStorage()

sub_folders_full_path = media_storage.GetSubFolderList(media_path)


def get_sub_folder_name(folder_full_path: List[str]) -> List[str]:
    """Get folder name from media storage."""
    folder_name_list = []
    for i in folder_full_path:
        split_folder_path_list = i.split("/")
        folder_name_list.append(split_folder_path_list[-1])
    return folder_name_list


# Create subfolder in media pool.
sub_folder_name = get_sub_folder_name(sub_folders_full_path)
media_pool = project.GetMediaPool()
root_folder = media_pool.GetRootFolder()
for i in sub_folder_name:
    media_pool.AddSubFolder(root_folder, i)
media_pool.AddSubFolder(root_folder, "_Timeline")

# Import footage from media storage.
all_clips = []  # a list of MediaPoolItems.
for count, sub_folder in enumerate(root_folder.GetSubFolderList()):
    media_pool.SetCurrentFolder(sub_folder)
    if sub_folder.GetName() == "_Timeline":
        break
    all_clips.append(media_storage.AddItemListToMediaPool(sub_folders_full_path[count]))

for sub_folder in root_folder.GetSubFolderList():
    # 排除 _Timeline 这个 Bin
    if sub_folder.GetName() == "_Timeline":
        break

    sub_folder_name = sub_folder.GetName()

    # clip_name_list = []
    # for clip in sub_folder.GetClipList():
    #     clip_name_list.append(clip.GetName())
    # clip_name_list.sort()
    if sub_folder.GetName() == "Ronin_4D#2":

        times = 0
        for clip in sub_folder.GetClipList():
            clip_width: int = int(clip.GetClipProperty()["Resolution"].split("x")[0])
            clip_height: int = int(clip.GetClipProperty()["Resolution"].split("x")[1])
            if clip_height == 1080:
                timeline_name = f"{sub_folder_name}_{str(clip_width)}x{str(clip_height)}"
                media_pool.SetCurrentFolder("_Timeline")
                media_pool.CreateEmptyTimeline(timeline_name)
                project.SetCurrentTimeline(timeline_name)
                timeline = project.GetCurrentTimeline()
                timeline.SetSetting("useCustomSettings", "1")
                timeline.SetSetting("timelineResolutionWidth", str(int(clip_width)))
                timeline.SetSetting("timelineResolutionHeight", str(int(clip_height)))
                timeline.SetSetting("timelineFrameRate", str(float(25)))
                media_pool.AppendToTimeline(clip)
            elif clip_width > 1080:
                timeline_name = f"{sub_folder_name}_{str(int(clip_width / 2))}x{str(int(clip_height / 2))}"
                media_pool.SetCurrentFolder("_Timeline")
                media_pool.CreateEmptyTimeline(timeline_name)

                timeline_number = project.GetTimelineCount()
                for i in range(timeline_number):
                    timeline = project.GetTimelineByIndex(i + 1)
                    project.SetCurrentTimeline(timeline)



                    if project.get_current_timeline().get_name().split("_")[2].split("x")[0] == clip_width:
                        timeline = project.GetCurrentTimeline()
                        print(timeline.GetName())
                        timeline.SetSetting("useCustomSettings", "1")
                        timeline.SetSetting("timelineResolutionWidth", str(int(clip_width / 2)))
                        timeline.SetSetting("timelineResolutionHeight", str(int(clip_height / 2)))
                        timeline.SetSetting("timelineFrameRate", str(float(25)))
                        media_pool.AppendToTimeline(clip)
                        times += 1
                        if times == len(sub_folder.GetClipList()) - 1:
                            break

    else:
        continue