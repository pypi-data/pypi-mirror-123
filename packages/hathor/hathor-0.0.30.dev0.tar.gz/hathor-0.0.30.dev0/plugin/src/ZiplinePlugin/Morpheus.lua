---@type Selection
local selection = game:GetService("Selection")

---@class Morpheus
local morpheus = {
	---@type BindableEvent
	Emitter = Instance.new("BindableEvent", script),
	UpdatingSelection = false
}

function morpheus:Init()
	selection.SelectionChanged:Connect(function()
		if self.UpdatingSelection then
			return
		end

		local containsScripts = false
		for _, v in pairs(selection:Get()) do
			if v:IsA("LuaSourceContainer") then
				containsScripts = true
				break
			end
		end

		self.Emitter:Fire("visibility", containsScripts)
	end)
end

---Morph
---@param instance LuaSourceContainer
---@param targetClassName string
function morpheus:Morph(instance, targetClassName)
	if not instance:IsA("LuaSourceContainer") then
		warn("Attempted to morph an instance that is not a LuaSourceContainer: " .. instance:GetFullName())
	end
	local parent = instance.Parent

	---@type LuaSourceContainer
	local newInstance = Instance.new(targetClassName)
	newInstance.Source = instance.Source
	newInstance.Name = instance.Name
	newInstance.Archivable = instance.Archivable

	pcall(function()
		newInstance.Disabled = instance.Disabled
	end)

	newInstance.Parent = parent
	for _, v in pairs(instance:GetChildren()) do
		v.Parent = newInstance
	end

	newInstance.Parent = parent
	instance:Destroy()

	return newInstance
end

function morpheus:MorphSelection(targetClassName)
	self.UpdatingSelection = true

	local s = selection:Get()
	local newScripts = {}

	for _, v in pairs(s) do
		if v:IsA("LuaSourceContainer") then
			table.insert(newScripts, self:Morph(v, targetClassName))
		end
	end

	local newSelection = {}
	for _, v in pairs(s) do
		if v and v.Parent then
			table.insert(newSelection, v)
		end
	end

	for _, v in pairs(newScripts) do
		table.insert(newSelection, v)
	end

	selection:Set(newSelection)

	self.UpdatingSelection = false
end

morpheus:Init()

return morpheus