---@type CoreGui
local coreGui = game:GetService("CoreGui")
---@type TextService
local textService = game:GetService("TextService")

---@type ZiplineAPI
local ZiplineAPI = require(script.Parent.ZiplineAPI)
---@type ZiplineWorker
local ZiplineWorker = require(script.Parent.ZiplineWorker)
---@type Morpheus
local Morpheus = require(script.Parent.Morpheus)

return function(plugin)
    local ziplineGui = {
        ---@type BindableEvent
        Emitter = Instance.new("BindableEvent", script)
    }

    local Theme = {
        BackgroundColor3 = Color3.new(0, 0, 0),
        TextColor3 = Color3.new(1, 1, 1)
    }
    ---@type BindableEvent
    Theme.Changed = Instance.new("BindableEvent", script)

    function Theme:Update(updaterFunction)
        if type(updaterFunction) == "function" then
            updaterFunction(self)
        end

        self.Changed:Fire(self)
    end

    local SettingsBag = {
        BaseURL = ZiplineAPI.BaseURL,
        CheckInterval = ZiplineWorker.CheckInterval
    }

    for k, v in pairs(SettingsBag) do
        local setting = plugin:GetSetting(k)
        SettingsBag[k] = setting or v
    end

    ---@type BindableEvent
    SettingsBag.Changed = Instance.new("BindableEvent", script)

    function SettingsBag:Update(updaterFunction)
        if type(updaterFunction) == "function" then
            updaterFunction(self)
        end

        self.Changed:Fire(self)
        ZiplineAPI.BaseURL = self.BaseURL
        ZiplineWorker.CheckInterval = self.CheckInterval

        for k, v in pairs(self) do
            local valueType = type(v)
            if valueType ~= "function" and valueType ~= "userdata" then
                plugin:SetSetting(k, v)
            end
        end
    end

    --- Creates a UIPadding object with all attributes set to the same size
    ---@param scale number
    ---@param offset number
    ---@return UIPadding
    local function uniformPadding(scale, offset)
        local dim = UDim.new(scale, offset)
        ---@type UIPadding
        local uiPadding = Instance.new("UIPadding")
        uiPadding.PaddingLeft = dim
        uiPadding.PaddingBottom = dim
        uiPadding.PaddingTop = dim
        uiPadding.PaddingRight = dim

        return uiPadding
    end

    local function hvPadding(scaleH, offsetH, scaleV, offsetV)
        local horizontal = UDim.new(scaleH, offsetH)
        local vertical = UDim.new(scaleV, offsetV)

        ---@type UIPadding
        local uiPadding = Instance.new("UIPadding")
        uiPadding.PaddingLeft = horizontal
        uiPadding.PaddingRight = horizontal
        uiPadding.PaddingBottom = vertical
        uiPadding.PaddingTop = vertical

        return uiPadding
    end

    ---@type ScreenGui
    local screenGui = Instance.new("ScreenGui")
    screenGui.ZIndexBehavior = Enum.ZIndexBehavior.Sibling
    screenGui.ResetOnSpawn = false
    screenGui.Name = "Zipline Plugin GUI"
    screenGui.Enabled = true

    ---@type Frame
    local rootFrame = Instance.new("Frame")
    rootFrame.Size = UDim2.new(0, 300, 0, 300)
    rootFrame.Position = UDim2.new(1, -320, 1, -320)
    rootFrame.BackgroundTransparency = 1
    rootFrame.BorderSizePixel = 0
    rootFrame.Parent = screenGui

    ---@type UIListLayout
    local rootListLayout = Instance.new("UIListLayout")
    rootListLayout.Padding = UDim.new(0, 5)
    rootListLayout.FillDirection = Enum.FillDirection.Horizontal
    rootListLayout.HorizontalAlignment = Enum.HorizontalAlignment.Right
    rootListLayout.SortOrder = Enum.SortOrder.LayoutOrder
    rootListLayout.Parent = rootFrame

    ---@type Frame
    local morphColumn = Instance.new("Frame")
    morphColumn.LayoutOrder = 1
    morphColumn.BackgroundTransparency = 1
    morphColumn.BorderSizePixel = 0
    morphColumn.Size = UDim2.new(0, 50, 1, 0)
    morphColumn.Visible = false
    morphColumn.Parent = rootFrame

    ---@type UIListLayout
    local morphList = Instance.new("UIListLayout")
    morphList.FillDirection = Enum.FillDirection.Vertical
    morphList.VerticalAlignment = Enum.VerticalAlignment.Bottom
    morphList.HorizontalAlignment = Enum.HorizontalAlignment.Center
    morphList.Padding = UDim.new(0, 5)
    morphList.SortOrder = Enum.SortOrder.LayoutOrder
    morphList.Parent = morphColumn

    local morphPadding = hvPadding(0, 5, 0, 35)
    morphPadding.Parent = morphColumn

    local morphButtonCount = 0
    local function addMorphButton(name, image, callback)
        ---@type ImageButton
        local button = Instance.new("ImageButton")
        button.Image = image or "rbxassetid://2131069071"
        button.Name = name
        button.BorderSizePixel = 0
        button.Size = UDim2.new(1, 0, 1, 0)
        button.SizeConstraint = Enum.SizeConstraint.RelativeXX
        button.LayoutOrder = morphButtonCount
        button.BackgroundTransparency = .2
        button.Parent = morphColumn

        button.MouseButton1Click:Connect(function(...)
            callback(name, ...)
        end)

        Theme.Changed.Event:Connect(function(theme)
            button.BackgroundColor3 = theme.BackgroundColor3
        end)

        morphButtonCount = morphButtonCount + 1
    end

    addMorphButton("ToScript", nil, function()
        Morpheus:MorphSelection("Script")
    end)

    addMorphButton("ToLocalScript", nil, function()
        Morpheus:MorphSelection("LocalScript")
    end)

    addMorphButton("ToModuleScript", nil, function()
        Morpheus:MorphSelection("ModuleScript")
    end)

    ---@type Frame
    local statusColumn = Instance.new("Frame")
    statusColumn.LayoutOrder = 0
    statusColumn.BackgroundTransparency = 1
    statusColumn.BorderSizePixel = 0
    statusColumn.Size = UDim2.new(0, 250, 1, 0)
    statusColumn.Parent = rootFrame

    ---@type UIListLayout
    local statusColumnList = Instance.new("UIListLayout")
    statusColumnList.Padding = UDim.new(0, 5)
    statusColumnList.FillDirection = Enum.FillDirection.Vertical
    statusColumnList.VerticalAlignment = Enum.VerticalAlignment.Bottom
    statusColumnList.SortOrder = Enum.SortOrder.LayoutOrder
    statusColumnList.Parent = statusColumn

    ---@type Frame
    local statusFrame = Instance.new("Frame")
    Theme.Changed.Event:Connect(function(theme)
        statusFrame.BackgroundColor3 = theme.BackgroundColor3
    end)
    statusFrame.LayoutOrder = 1
    statusFrame.BackgroundTransparency = .3
    statusFrame.BorderSizePixel = 0
    statusFrame.Size = UDim2.new(1, 0, 0, 30)
    statusFrame.Parent = statusColumn

    local mainFramePadding = uniformPadding(0, 5)
    mainFramePadding.Parent = statusFrame

    ---@type UIListLayout
    local statusFrameList = Instance.new("UIListLayout")
    statusFrameList.FillDirection = Enum.FillDirection.Horizontal
    statusFrameList.Padding = UDim.new(0, 5)
    statusFrameList.HorizontalAlignment = Enum.HorizontalAlignment.Right
    statusFrameList.SortOrder = Enum.SortOrder.LayoutOrder
    statusFrameList.Parent = statusFrame

    ---@type ImageButton
    local settingsButton = Instance.new("ImageButton")
    settingsButton.Size = UDim2.new(1, 0, 1, 0)
    settingsButton.BorderSizePixel = 0
    settingsButton.SizeConstraint = Enum.SizeConstraint.RelativeYY

    ---@type ImageLabel
    local statusImage = Instance.new("ImageLabel")
    statusImage.Size = settingsButton.Size
    statusImage.BorderSizePixel = 0
    statusImage.BackgroundTransparency = 1
    statusImage.SizeConstraint = settingsButton.SizeConstraint
    statusImage.Image = "rbxassetid://2133301260"

    ---@type TextLabel
    local statusLabel = Instance.new("TextLabel")
    statusLabel.BorderSizePixel = 0
    statusLabel.BackgroundTransparency = 1
    statusLabel.Size = UDim2.new(0, 150, 1, 0)
    Theme.Changed.Event:Connect(function(theme)
        statusLabel.TextColor3 = theme.TextColor3
    end)

    local function setStatusText(text)
        statusLabel.Text = tostring(text)
        local textSize = textService:GetTextSize(
            text,
            statusLabel.TextSize,
            statusLabel.Font,
            Vector2.new(200, 30)
        )

        statusLabel.Size = UDim2.new(0, textSize.x, 1, 0)
    end
    setStatusText("Waiting for instructions")

    local frameItemCounter = 0
    ---addToFrame
    ---@param inst GuiObject
    local function addToFrame(inst)
        inst.LayoutOrder = frameItemCounter
        inst.Parent = statusFrame
        frameItemCounter = frameItemCounter + 1
    end

    addToFrame(statusLabel)
    addToFrame(statusImage)
    addToFrame(settingsButton)

    ---

    ---@type Frame
    local settingsFrame = Instance.new("Frame")
    Theme.Changed.Event:Connect(function(theme)
        settingsFrame.BackgroundColor3 = theme.BackgroundColor3
    end)
    settingsFrame.LayoutOrder = 0
    settingsFrame.BackgroundTransparency = statusFrame.BackgroundTransparency
    settingsFrame.BorderSizePixel = 0
    settingsFrame.Size = UDim2.new(1, 0, 0, 175)
    settingsFrame.Visible = false
    settingsFrame.Parent = statusColumn

    local settingsFramePadding = uniformPadding(0, 5)
    settingsFramePadding.Parent = settingsFrame

    local settingsTitleHeight = 25
    ---@type TextLabel
    local settingsTitle = Instance.new("TextLabel")
    Theme.Changed.Event:Connect(function(theme)
        settingsTitle.TextColor3 = theme.TextColor3
    end)
    settingsTitle.BackgroundTransparency = 1
    settingsTitle.BorderSizePixel = 0
    settingsTitle.Position = UDim2.new(0, 0, 0, 0)
    settingsTitle.Size = UDim2.new(1, 0, 0, settingsTitleHeight)
    settingsTitle.Text = "Settings"
    settingsTitle.TextXAlignment = Enum.TextXAlignment.Left
    settingsTitle.TextYAlignment = Enum.TextYAlignment.Top
    settingsTitle.Parent = settingsFrame

    ---@type Frame
    local settingsContainer = Instance.new("Frame")
    settingsContainer.Position = UDim2.new(0, 0, 0, settingsTitleHeight)
    settingsContainer.Size = UDim2.new(1, 0, 1, -settingsTitleHeight)
    settingsContainer.BackgroundTransparency = 1
    settingsContainer.BorderSizePixel = 0
    settingsContainer.Parent = settingsFrame

    ---@type UIListLayout
    local settingsList = Instance.new("UIListLayout")
    settingsList.Padding = UDim.new(0, 0)
    settingsList.SortOrder = Enum.SortOrder.LayoutOrder
    settingsList.Parent = settingsContainer

    local settingsListItemCounter = 0
    ---addToSettingsContainer
    ---@param item GuiObject
    local function addToSettingsContainer(item)
        item.LayoutOrder = settingsListItemCounter
        item.Parent = settingsContainer
        settingsListItemCounter = settingsListItemCounter + 1
    end

    local function settingsListLabel(text)
        ---@type TextLabel
        local label = Instance.new("TextLabel")
        label.BackgroundTransparency = 1
        label.BorderSizePixel = 0
        label.Size = UDim2.new(1, 0, 0, 20)
        label.TextXAlignment = Enum.TextXAlignment.Left
        label.Text = text

        Theme.Changed.Event:Connect(function(theme)
            label.TextColor3 = theme.TextColor3
        end)

        addToSettingsContainer(label)
        return label
    end

    local function settingsListInput(name)
        ---@type TextBox
        local box = Instance.new("TextBox")
        box.Name = "Settings list input: " .. name
        box.PlaceholderText = name
        box.Size = UDim2.new(1, 0, 0, 20)
        box.BorderSizePixel = 0
        box.BackgroundTransparency = .3
        box.ClearTextOnFocus = false

        Theme.Changed.Event:Connect(function(theme)
            box.BackgroundColor3 = theme.BackgroundColor3
            box.TextColor3 = theme.TextColor3
        end)

        addToSettingsContainer(box)
        return box
    end

    settingsListLabel("Server URL")
    local serverUrlBox = settingsListInput("Server URL")
    addToSettingsContainer(serverUrlBox)
    settingsListLabel("Check interval")
    local intervalBox = settingsListInput("Check Interval")
    addToSettingsContainer(intervalBox)

    SettingsBag.Changed.Event:Connect(function(settings)
        serverUrlBox.Text = settings.BaseURL
        intervalBox.Text = tostring(settings.CheckInterval)
    end)

    ---@type Frame
    local settingsButtonRow = Instance.new("Frame")
    settingsButtonRow.BackgroundTransparency = 1
    settingsButtonRow.BorderSizePixel = 0
    settingsButtonRow.Size = UDim2.new(1, 0, 0, 40)
    addToSettingsContainer(settingsButtonRow)

    local settingsButtonRowPadding = uniformPadding(0, 5)
    settingsButtonRowPadding.Parent = settingsButtonRow

    ---@type UIListLayout
    local settingsButtonRowList = Instance.new("UIListLayout")
    settingsButtonRowList.SortOrder = Enum.SortOrder.LayoutOrder
    settingsButtonRowList.HorizontalAlignment = Enum.HorizontalAlignment.Right
    settingsButtonRowList.Parent = settingsButtonRow

    ---@type TextButton
    local saveButton = Instance.new("TextButton")
    saveButton.Size = UDim2.new(0, 50, 1, 0)
    saveButton.Text = "Save"
    saveButton.BorderSizePixel = 0
    saveButton.BackgroundTransparency = .3
    saveButton.Parent = settingsButtonRow

    saveButton.MouseButton1Click:Connect(function()
        SettingsBag:Update(function(settings)
            settings.BaseURL = serverUrlBox.Text
            settings.CheckInterval = tonumber(intervalBox.Text) or settings.CheckInterval
        end)
    end)

    Theme.Changed.Event:Connect(function(theme)
        saveButton.BackgroundColor3 = theme.BackgroundColor3
        saveButton.TextColor3 = theme.TextColor3
    end)

    if (coreGui:FindFirstChild(screenGui.Name)) then
        while coreGui:FindFirstChild(screenGui.Name) do
            coreGui:FindFirstChild(screenGui.Name):Destroy()
        end
    end

    screenGui.Parent = coreGui

    function ziplineGui:Toggle()
        screenGui.Enabled = not screenGui.Enabled
    end

    function ziplineGui:Show()
        screenGui.Enabled = true
    end

    settingsButton.MouseButton1Click:Connect(function()
        settingsFrame.Visible = not settingsFrame.Visible
    end)

    ZiplineAPI.Emitter.Event:Connect(function(s, value)
        if s == "announcing" then
            setStatusText("Announcing to server...")
        elseif s == "announced" then
            setStatusText(value and "Announced to server" or "Failed to announce")
        elseif s == "leaving" then
            setStatusText("Disconnecting...")
        elseif s == "left" then
            setStatusText(value and "Disconnected" or "Failed to disconnect")
        end
    end)

    ZiplineWorker.Emitter.Event:Connect(function(s, value)
        if s == "receiving" then
            setStatusText("Fetching changes")
        elseif s == "applying" then
            setStatusText(string.format("Applying %d changes...", value))
        elseif s == "applied" then
            setStatusText("Applied changes (Waiting)")
        end
    end)

    Morpheus.Emitter.Event:Connect(function(s, v)
        if s == "visibility" then
            morphColumn.Visible = v
        end
    end)

    Theme:Update(nil)
    SettingsBag:Update(nil)

    return ziplineGui
end
