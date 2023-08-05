---@entrypoint Script game.ZiplinePlugin.ZiplinePluginScript

local ZiplineAPI = require(script.Parent.ZiplineAPI)
local ZiplineWorker = require(script.Parent.ZiplineWorker)
local ZiplineGui = require(script.Parent.ZiplineGui)(plugin)
local serializeInstance = require(script.Parent.serializeInstance)

local ServerStorage = game:GetService("ServerStorage")
local Selection = game:GetService("Selection")

function killZipline()
    ZiplineWorker:Stop()
    ZiplineAPI:Leave()
end

local toolbar = plugin:CreateToolbar("Zipline")
local buttons = {}

buttons.start = toolbar:CreateButton("Start Zipline", "Start the zipline", "rbxassetid://2131069071")
buttons.stop = toolbar:CreateButton("Stop Zipline", "Stop the zipline", "rbxassetid://2131069135")
buttons.saveSelection = toolbar:CreateButton("Save Selection", "Save selection to disk", "rbxassetid://6733115090")
buttons.toggle = toolbar:CreateButton("Toggle Zipline GUI", "Toggles the Zipline syncing plugin", "rbxassetid://2133301260")

buttons.start.Click:Connect(function()
    ZiplineAPI:Announce("Roblox Studio")
    ZiplineWorker:Start()

    ZiplineGui:Show()
end)

buttons.stop.Click:Connect(function()
    killZipline()
end)

buttons.saveSelection.Click:Connect(function()
    for _, instance in pairs(Selection:Get()) do
        print("> Saving", instance:GetFullName())

        ZiplineAPI:SaveInstance(
            instance:GetFullName(),
            serializeInstance(instance)
        )
    end

    print("Saved selection!")
end)

buttons.toggle.Click:Connect(function()
    ZiplineGui:Toggle()
end)

local ksName = "Zipline Killswitch"
local killswitch = ServerStorage:FindFirstChild(ksName)

if not killswitch then
    killswitch = Instance.new("BoolValue")
    killswitch.Name = ksName
    killswitch.Archivable = false
    killswitch.Parent = ServerStorage
else
    killswitch.Value = true
    wait(.1)
    killswitch.Value = false
end

killswitch.Changed:Connect(function()
    if killswitch.Value then
        killZipline()
    end
end)
