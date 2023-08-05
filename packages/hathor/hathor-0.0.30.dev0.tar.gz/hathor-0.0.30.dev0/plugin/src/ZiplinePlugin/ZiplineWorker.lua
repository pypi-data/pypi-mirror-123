local ZiplineAPI = require(script.Parent.ZiplineAPI)

---@class ZiplineWorker
local ZiplineWorker = {
    Running = false,
    CheckInterval = .5,
    PackageSize = 10,
    ChangeRef = {},
    ---@type BindableEvent
    Emitter = Instance.new("BindableEvent", script)
}

function ZiplineWorker:Start()
    self.Running = true

    spawn(function()
        while self.Running and ZiplineAPI.Announced do
            if self.Package then
                self:ReceivePackage()
            else
                self:FetchChangeList()
            end

            wait(self.CheckInterval)
        end
    end)
end

function ZiplineWorker:FetchChangeList()
    local changelist = ZiplineAPI:GetChangelist()
    if #changelist > 0 then
        local packageContents = {}
        local changeRef = {}

        for i = 1, math.min(self.PackageSize, #changelist), 1 do
            table.insert(packageContents, changelist[i].id)
            changeRef[changelist[i].id] = changelist[i]
        end

        local packageId = ZiplineAPI:CreatePackage(packageContents)
        self.ChangeRef = changeRef
        self.Package = packageId
    end
end

function ZiplineWorker:ReceivePackage()
    self.Emitter:Fire("receiving")

    local package = ZiplineAPI:GetPackage(self.Package)

    if not package then
        warn("Invalid package " .. tostring(self.Package))
        ZiplineAPI:DeletePackage(self.Package)
        self.Package = nil

        return
    end

    self.Emitter:Fire("applying", package.packageSize)

    local appliedChanges = {}
    for changeId, content in pairs(package.content) do
        local change = self.ChangeRef[changeId]
        if change then
            self:ApplyChange(change, content)
            table.insert(appliedChanges, changeId)
            self.Emitter:Fire("applying", package.packageSize - #appliedChanges)
        end
    end

    ZiplineAPI:DeleteChanges(appliedChanges)

    if package.remainingChanges <= 0 then
        ZiplineAPI:DeletePackage(self.Package)
        self.Package = nil
    end

    self.Emitter:Fire("applied")
end

function ZiplineWorker:ApplyChange(change, content)
    local instance = game

    for i = 1, #change.path, 1 do
        local component = change.path[i]

        if i >= #change.path then
            local ending = component:sub(#component - 3)
            if ending and ending:lower() == ".lua" then
                component = component:sub(1, #component - 4)
            end
        end

        local up = instance
        if not instance and change.kind == "ENTRY_DELETE" then
            return
        end
        instance = instance:FindFirstChild(component)

        if not instance and change.kind ~= "ENTRY_DELETE" then
            if i == #change.path and not change.directory then
                instance = Instance.new("ModuleScript")
                instance.Name = component
                instance.Source = content
                instance.Parent = up
            else
                instance = Instance.new("Folder")
                instance.Name = component
                instance.Parent = up
            end
        end
    end

    if instance then
        if change.kind == "ENTRY_DELETE" then
            instance:Destroy()
        elseif change.kind == "ENTRY_MODIFY" or change.kind == "ENTRY_CREATE" then
            if instance:IsA("LuaSourceContainer") then
                instance.Source = content
            end
        end
    end
end

function ZiplineWorker:Stop()
    self.Package = nil
    self.Running = false
end

return ZiplineWorker
