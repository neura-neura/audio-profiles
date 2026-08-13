from pathlib import Path
p = Path(r"C:\Users\neura\repos\audio-device-switcher\src\AudioProfiles\App.xaml")
p.write_text("""<?xml version=\"1.0\" encoding=\"utf-8\"?>
<Application
    x:Class=\"AudioProfiles.App\"
    xmlns=\"http://schemas.microsoft.com/winfx/2006/xaml/presentation\"
    xmlns:x=\"http://schemas.microsoft.com/winfx/2006/xaml\"
    xmlns:local=\"using:AudioProfiles\">
    <Application.Resources>
        <ResourceDictionary>
            <ResourceDictionary.MergedDictionaries>
                <XamlControlsResources xmlns=\"using:Microsoft.UI.Xaml.Controls\" />
            </ResourceDictionary.MergedDictionaries>
            <SolidColorBrush x:Key=\"BrandTealBrush\" Color=\"#0F6B6B\" />
            <SolidColorBrush x:Key=\"BrandAmberBrush\" Color=\"#E8A317\" />
            <SolidColorBrush x:Key=\"ActiveFillBrush\" Color=\"#1A0F6B6B\" />
            <Thickness x:Key=\"PagePadding\">24,12,24,24</Thickness>

            <Style x:Key=\"PageTitleStyle\" TargetType=\"TextBlock\" BasedOn=\"{StaticResource SubtitleTextBlockStyle}\">
                <Setter Property=\"TextWrapping\" Value=\"Wrap\" />
            </Style>
            <Style x:Key=\"SectionBodyStyle\" TargetType=\"TextBlock\" BasedOn=\"{StaticResource BodyTextBlockStyle}\">
                <Setter Property=\"Opacity\" Value=\"0.82\" />
            </Style>
        </ResourceDictionary>
    </Application.Resources>
</Application>
""", encoding="utf-8")
print("wrote App.xaml")
