from pathlib import Path
p = Path(r'C:\\Users\\neura\\repos\\audio-device-switcher\\src\\AudioProfiles\\AudioProfiles.csproj')
text = p.read_text(encoding='utf-8')
block = '''  <ItemGroup>
    <Content Update="Assets\\**\\*">
      <CopyToOutputDirectory>PreserveNewest</CopyToOutputDirectory>
      <CopyToPublishDirectory>PreserveNewest</CopyToPublishDirectory>
    </Content>
  </ItemGroup>
'''
insert = '''  <ItemGroup>
    <Content Update="Assets\\**\\*">
      <CopyToOutputDirectory>PreserveNewest</CopyToOutputDirectory>
      <CopyToPublishDirectory>PreserveNewest</CopyToPublishDirectory>
    </Content>
  </ItemGroup>

  <ItemGroup Condition="$(RuntimeIdentifier.Contains('arm64'))">
    <None Include="Runtime\\win-arm64\\Microsoft.WindowsAppRuntime.Insights.Resource.dll">
      <CopyToOutputDirectory>PreserveNewest</CopyToOutputDirectory>
      <CopyToPublishDirectory>PreserveNewest</CopyToPublishDirectory>
      <Link>Microsoft.WindowsAppRuntime.Insights.Resource.dll</Link>
      <TargetPath>Microsoft.WindowsAppRuntime.Insights.Resource.dll</TargetPath>
    </None>
  </ItemGroup>
  <ItemGroup Condition="!$(RuntimeIdentifier.Contains('arm64'))">
    <None Include="Runtime\\win-x64\\Microsoft.WindowsAppRuntime.Insights.Resource.dll">
      <CopyToOutputDirectory>PreserveNewest</CopyToOutputDirectory>
      <CopyToPublishDirectory>PreserveNewest</CopyToPublishDirectory>
      <Link>Microsoft.WindowsAppRuntime.Insights.Resource.dll</Link>
      <TargetPath>Microsoft.WindowsAppRuntime.Insights.Resource.dll</TargetPath>
    </None>
  </ItemGroup>
'''
if block not in text:
    raise SystemExit('content assets block not found')
p.write_text(text.replace(block, insert, 1), encoding='utf-8')
print('csproj updated')
