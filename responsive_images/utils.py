


def get_final_resolution(resolution, resolutions):
    if resolution > resolutions[0]:
        resolutions[0]

    else:
        for r in resolutions:
            if resolution > r:
                final_resolution = r
                break
    if resolution < resolutions[len(resolutions)-1]:
        final_resolution = resolutions[len(resolutions)-1]
        #final_resolution = resolution
    final_resolution = final_resolution-100
    return final_resolution
