using System.Globalization;

namespace AudioProfiles.Helpers;

public static class Loc
{
    public static string Get(string key)
    {
        var spanish = CultureInfo.CurrentUICulture.TwoLetterISOLanguageName.Equals("es", StringComparison.OrdinalIgnoreCase);
        var table = spanish ? StringCatalog.Spanish : StringCatalog.English;
        return table.TryGetValue(key, out var value) ? value : key;
    }

    public static string Format(string key, params object[] args)
    {
        try
        {
            return string.Format(Get(key), args);
        }
        catch
        {
            return Get(key);
        }
    }
}
