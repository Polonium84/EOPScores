using System;
using Newtonsoft.Json;
using Microsoft.Data.Sqlite;

namespace EOPScoresScanner
{
    class EOPScoresScanner
    {
        static void Main(string[] args)
        {
            string RootDir = @"F:\EOPScores";

            Console.WriteLine("Hello World!");
        }
    }
    class _EOP_CLASS
    {
        static string[] _Classes =
        {
            "流行",
            "影视",
            "经典",
            "动漫",
            "儿歌",
            "练习曲",
            "轻音乐",
            "原创",
            "民乐",
            "其他"
        };
        static bool _Contains(string name)
        {
            foreach (string s in _Classes)
                if (s == name)
                    return true;
            return false;
        }
    }
}
