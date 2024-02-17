main.py can be executed in two parts as follows:
```
python3 main.py <part id> <img dir> <output csv>
```
There are two tasks:

  * For the first part, the code iterates through all the images in the given directory and generates a csv file specifying the various parameters that are calculated. It has the following columns : image name, number of sutures,
mean inter suture spacing, variance of inter suture spacing, mean suture angle wrt x-axis, variance of suture angle wrt x-axis. main.py will be
executed as follows:
    ```
    python3 main.py 1 <img dir> <output csv>
    ```

  * For the second part, we have pairs of images and we need to output which image is a better suture outcome with respect to inter-suture distance and angulation of sutures. main.py will be executed as follows:
    ```
    python3 main.py 2 <input csv> <output csv>
    ```
The input csv file has the following two columns: img1 path, img2 path, where
as output csv would have the following four columns: img1 path, img2 path,
output distance, output angle, where output distance and output angle take
the values either 1 or 2, depending upon which image is better with respect to that
feature.
Here we have some sample test images from the [AIIMS image dataset](http://aiimsnets.org/microsuturing.asp).  
Also added a sample ***input.csv*** for 2nd part.
