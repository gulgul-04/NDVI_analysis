import ee

def mask_clouds_s2(image, cloud_threshold=30):

    # Create a cloud mask based on the QA60 band and optional cloud probability band
    qa = image.select('QA60')
    cloud_bit_mask = 1 << 10
    cirrus_bit_mask = 1 << 11

    mask = qa.bitwiseAnd(cloud_bit_mask).eq(0).And(qa.bitwiseAnd(cirrus_bit_mask).eq(0))

    #try to mask usig cloud probability band if it exists
    def mask_with_cldprb(img):
        return img.updateMask(mask.And(img.select('CLDPRB').lt(cloud_threshold)))
    
    def mask_without_cldprb(img):
        return img.updateMask(mask)

    # Use ee.Algorithms.If to branch, checking for CLDPRB in bandNames (still server-side!)
    img_out = ee.Image(
        ee.Algorithms.If(
            image.bandNames().contains('CLDPRB'),
            mask_with_cldprb(image),
            mask_without_cldprb(image)
        )
    )

    return img_out