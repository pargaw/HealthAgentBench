Review the MRI in `/workspace/mri/` and answer:

- `abnormal`: Is any abnormality present, including findings other than tears?
  The reference label reflects a radiologist's clinical report. An exam is
  abnormal only if the report described an abnormal finding.
- `acl`: Is there an anterior cruciate ligament (ACL) tear? Count partial and
  complete tears; exclude isolated sprain, mucoid degeneration, and ganglion cyst.
- `meniscus`: Is there a meniscal tear? Count increased signal reaching a joint
  surface on at least two slices, or meniscal deformity. Exclude degeneration
  and postoperative changes without a tear.

Review the axial, coronal, and sagittal MRI series. For each plane:

- `<plane>_contact_sheet.jpg`: labeled overview of all slices (lossy JPEG).
- `<plane>/slice_*.png`: lossless 256 x 256 images, one per slice.
- `<plane>.npy`: the same slice pixels as a uint8 NumPy array shaped
  `[number_of_slices, 256, 256]`, indexed `[slice, row, column]`.

PNGs and arrays preserve the full available resolution. Use them for pixel
detail rather than the JPEG overview.
NumPy, Pillow, and Matplotlib are installed.

Save `/workspace/submission.json` with exactly the keys `abnormal`, `acl`, and
`meniscus`, each set to integer `1` (present) or `0` (absent). All three answers
must match the reference labels to pass.

## Rules

Answer from the supplied images only. Do not search the web for, download, or use
any external dataset, label file or other resource
that could reveal or predict the reference labels for this examination.

## Resources

You have 1 hour to complete the task. The container is configured for 2 CPUs,
4 GiB of memory, 10 GiB of disk, and no GPU. System tools may report host resources;
use these limits when planning your work.
