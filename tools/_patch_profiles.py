from pathlib import Path
p = Path(r'C:\\Users\\neura\\repos\\audio-device-switcher\\src\\AudioProfiles\\Views\\ProfilesPage.xaml')
p.write_text('''<?xml version="1.0" encoding="utf-8" ?>
<Page
    x:Class="AudioProfiles.Views.ProfilesPage"
    xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
    xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml">

    <Grid Padding="{StaticResource PagePadding}">
        <Grid.RowDefinitions>
            <RowDefinition Height="Auto" />
            <RowDefinition Height="*" />
        </Grid.RowDefinitions>

        <Grid>
            <Grid.ColumnDefinitions>
                <ColumnDefinition Width="*" />
                <ColumnDefinition Width="Auto" />
            </Grid.ColumnDefinitions>
            <StackPanel Spacing="4">
                <TextBlock x:Name="TitleText" Style="{StaticResource PageTitleStyle}" />
                <TextBlock x:Name="CurrentProfileText" Style="{StaticResource SectionBodyStyle}" />
            </StackPanel>
            <StackPanel Grid.Column="1" Orientation="Horizontal" Spacing="8">
                <Button x:Name="RefreshButton" Click="RefreshButton_Click" />
                <Button x:Name="AddButton" Style="{StaticResource AccentButtonStyle}" Click="AddButton_Click" />
            </StackPanel>
        </Grid>

        <Grid Grid.Row="1" Margin="0,16,0,0">
            <StackPanel
                x:Name="EmptyState"
                MaxWidth="560"
                HorizontalAlignment="Center"
                VerticalAlignment="Center"
                Spacing="12"
                Visibility="Collapsed">
                <FontIcon FontSize="32" Glyph="&#xE8D6;" Foreground="{StaticResource BrandTealBrush}" />
                <TextBlock x:Name="EmptyTitle" Style="{StaticResource PageTitleStyle}" HorizontalAlignment="Center" TextAlignment="Center" />
                <TextBlock x:Name="EmptyBody" Style="{StaticResource SectionBodyStyle}" HorizontalAlignment="Center" TextAlignment="Center" />
                <Button x:Name="EmptyCreateButton" HorizontalAlignment="Center" Style="{StaticResource AccentButtonStyle}" Click="AddButton_Click" />
            </StackPanel>

            <ListView
                x:Name="ProfileList"
                IsItemClickEnabled="True"
                ItemClick="ProfileList_ItemClick"
                SelectionMode="None">
                <ListView.ItemContainerStyle>
                    <Style TargetType="ListViewItem">
                        <Setter Property="HorizontalContentAlignment" Value="Stretch" />
                        <Setter Property="Padding" Value="0,0,0,8" />
                    </Style>
                </ListView.ItemContainerStyle>
                <ListView.ItemTemplate>
                    <DataTemplate>
                        <Border
                            Padding="16"
                            Background="{Binding CardBrush}"
                            BorderBrush="{Binding BorderBrush}"
                            BorderThickness="1"
                            CornerRadius="12">
                            <Grid ColumnSpacing="12">
                                <Grid.ColumnDefinitions>
                                    <ColumnDefinition Width="Auto" />
                                    <ColumnDefinition Width="*" />
                                    <ColumnDefinition Width="Auto" />
                                </Grid.ColumnDefinitions>
                                <Border
                                    Width="40"
                                    Height="40"
                                    Background="{StaticResource BrandTealBrush}"
                                    CornerRadius="10">
                                    <FontIcon
                                        HorizontalAlignment="Center"
                                        VerticalAlignment="Center"
                                        FontSize="18"
                                        Foreground="White"
                                        Glyph="{Binding Glyph}" />
                                </Border>
                                <StackPanel Grid.Column="1" VerticalAlignment="Center" Spacing="2">
                                    <StackPanel Orientation="Horizontal" Spacing="8">
                                        <TextBlock FontSize="16" FontWeight="SemiBold" Text="{Binding Name}" />
                                        <Border
                                            Padding="8,2"
                                            Background="{StaticResource BrandAmberBrush}"
                                            CornerRadius="999"
                                            Visibility="{Binding ActiveVisibility}">
                                            <TextBlock FontSize="12" FontWeight="SemiBold" Text="{Binding ActiveLabel}" />
                                        </Border>
                                    </StackPanel>
                                    <TextBlock Opacity="0.82" Text="{Binding DeviceSummary}" TextWrapping="Wrap" />
                                    <TextBlock FontSize="12" Opacity="0.7" Text="{Binding StatusText}" TextWrapping="Wrap" />
                                </StackPanel>
                                <StackPanel Grid.Column="2" VerticalAlignment="Center" Spacing="6">
                                    <Button
                                        Click="EditButton_Click"
                                        Content="{Binding ActionLabel}"
                                        Tag="{Binding Id}" />
                                    <Button
                                        Click="DeleteButton_Click"
                                        Content="{Binding DeleteLabel}"
                                        Tag="{Binding Id}" />
                                </StackPanel>
                            </Grid>
                        </Border>
                    </DataTemplate>
                </ListView.ItemTemplate>
            </ListView>
        </Grid>
    </Grid>
</Page>
''', encoding='utf-8')
print('ProfilesPage.xaml written', p.stat().st_size)
