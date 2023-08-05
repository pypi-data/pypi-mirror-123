---@entrypoint Script ServerScriptService.ExampleServer
local items = require("Core.ItemDB")

for _, item in pairs(items) do
    print(item.ID, item.Name)
end

print("Hello Roblox :D")

local baseplate = require("Instances.Workspace.Baseplate.instance.yml")
local me = require("Instances.Workspace.Brinker7.instance.yml")

if not game.Workspace:FindFirstChild("Baseplate") then
    baseplate.Parent = game.Workspace
end

while wait(1) do
    me:Clone().Parent = game:GetService("Workspace")
end
