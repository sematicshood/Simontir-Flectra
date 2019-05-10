<?php

define('ESC', chr(27));
define('LF', chr('0x0a'));
define('NUL', chr('0x00'));

class System
{
    const OS_UNKNOWN = 1;
    const OS_WIN = 2;
    const OS_LINUX = 3;
    const OS_OSX = 4;

    static public function getOS()
    {
        switch (true) {
            case stristr(PHP_OS, 'DAR'):
                return self::OS_OSX;
            case stristr(PHP_OS, 'WIN'):
                return self::OS_WIN;
            case stristr(PHP_OS, 'LINUX'):
                return self::OS_LINUX;
            default:
                return self::OS_UNKNOWN;
        }
    }
}

class RawPrinter
{
    var $printername;
    var $osname;

    function __construct($printername = 'Generic Printer')
    {
        $this->printername = $printername;
        $this->osname = System::getOS();
    }

    public function openPrinter()
    {
        if ($this->osname == System::OS_WIN) {
            $handle = printer_open($this->printername);
            printer_set_option($handle, 'PRINTER_MODE', 'text');
            printer_set_option($handle, 'PRINTER_COPIES', 1);
            printer_set_option($handle, 'PRINTER_PAPER_FORMAT', PRINTER_FORMAT_A4);
            printer_set_option($handle, 'PRINTER_TEXT_COLOR', '005533');
            printer_set_option($handle, 'PRINTER_TEXT_ALIGN', PRINTER_TA_BASELINE);
        } else { }
    }

    public function writePrinter($handle, $data)
    {
        if ($this->osname == System::OS_WIN) {
            $ret = printer_write($handle, $data);
            return $ret;
        }
    }

    public function send($data, $shopname = '', $company_name = '')
    {
        if ($this->osname == System::OS_WIN) {
            $handle = $this->openPrinter();
            $ret = $this->writePrinter($handle, $data);
            $this->closePrinter($handle);
            return $ret;
        } else {
            system("echo $data > $this->printername");
        }
    }
}
